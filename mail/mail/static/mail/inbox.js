document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

})

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('form').onsubmit = function() {

    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value ,
        subject: document.querySelector('#compose-subject').value ,
        body: document.querySelector('#compose-body').value
    })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    load_mailbox('sent');
    return false;
    }
}

function reply_email(recipients, subject, body, timestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-body').value = `On ${timestamp} ${recipients} wrote: ${body}`;

  if (subject.slice(0, 3) === "Re:") {
    document.querySelector('#compose-subject').value = subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
  }

  document.querySelector('form').onsubmit = function() {

    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value ,
        subject: document.querySelector('#compose-subject').value ,
        body: document.querySelector('#compose-body').value
    })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    load_mailbox('sent');
    return false;
    }
}

function load_mailbox(mailbox) {

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      emails.forEach(mail => {

        const div = document.createElement('button');
        div.className = "mail";
        div.id = mail.id;
        if (mail.read === true) {
          div.style = "background-color: white;";
        } else {
          div.style = "background-color: rgb(177, 177, 177);";
        }
        div.addEventListener('click', function() {
          fetch(`/emails/${this.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          getMail(this.id);
        });
        document.querySelector("#emails-view").append(div); 
        
        const sender = document.createElement('span');
        sender.innerHTML = mail.sender;
        sender.id = "mail-sender";
        document.getElementById(mail.id).append(sender);

        const subject = document.createElement('span');
        subject.innerHTML = mail.subject;
        subject.id = "mail-subject";
        document.getElementById(mail.id).append(subject);

        const time = document.createElement('span');
        time.innerHTML = mail.timestamp;
        time.id = "mail-time";
        document.getElementById(mail.id).append(time);
        
      });
  });
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}

function getMail(id) {

  document.querySelector("#mail-view").innerHTML = "";
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(mail => {

      const sender = document.createElement('div');
      sender.innerHTML = `<strong>Form:</strong> ${mail.sender}`;
      document.querySelector("#mail-view").append(sender);

      const to = document.createElement('div');
      to.innerHTML = "<strong>To:</strong> ";
      mail.recipients.forEach(element => {
        to.innerHTML += `${element}, `;
      });
      to.innerHTML = to.innerHTML.slice(0, -2);
      document.querySelector("#mail-view").append(to);

      const subject = document.createElement('div');
      subject.innerHTML = `<strong>Subject:</strong> ${mail.subject}`;
      document.querySelector("#mail-view").append(subject);

      const time = document.createElement('div');
      time.innerHTML = `<strong>Timestamp:</strong> ${mail.timestamp}`;
      document.querySelector("#mail-view").append(time);
      
      const hr = document.createElement('hr')
      document.querySelector("#mail-view").append(hr);

      const body = document.createElement('div');
      body.innerHTML = mail.body;
      body.className = "fade";
      body.style = "padding-bottom: 10px;";
      document.querySelector("#mail-view").append(body);

      

      if (document.querySelector("#user").innerHTML !== mail.sender) {
        const element = document.createElement('button');
        element.className = "btn btn-sm btn-outline-primary fade";
        element.style = "margin-right: 5px;";
        if (mail.archived === false) {
          element.innerHTML = 'Archive';
        } else {
          element.innerHTML = 'Unarchive';
        }      
        element.id = mail.id;
        document.querySelector('#mail-view').append(element);
        
        element.addEventListener('click', function() {
          if (element.innerHTML === "Archive") {
            element.innerHTML = "Unarchive";
            fetch(`/emails/${this.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: true
              })
            })
          } else {
            element.innerHTML = "Archive";
            fetch(`/emails/${this.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: false
              })
            })
          }
          load_mailbox('inbox');     
        });
      }

      const reply = document.createElement('button');
      reply.innerHTML = "Reply";
      reply.className = "btn btn-sm btn-outline-primary fade";
      reply.addEventListener('click', () => {
        reply_email(to.innerHTML.slice(21), mail.subject, mail.body, mail.timestamp);
      })
      document.querySelector("#mail-view").append(reply);
  });

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';
}