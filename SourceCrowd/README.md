# SourceCrowd
## Video Demo:  <https://youtu.be/gntt5gtyiGY>


## Description:


SourceCrowd is a web application that lets you discover the real web. In the sense that it doesn't relies on any kind of search index. In this application, people add links to the webpages that they find are helpful. They can also add a title for that link, based on which people can search for that webpage. Often the title in the HTML file of webpages, based on which the traditional search engines extract search results, are hard to decide based on a common person's intellect about what terms he will use to search that kind of webpage. This often leads to misleading results by search engines. On SourceCrowd, when people add links, they will also be able to add a title in common person's terms which they usually search for in order to find that respective webpage. They will also be able to add a description of 280 characters which will add to understanding of that webpage's description.


The idea for SourceCrowd stemmed from the fact that I never knew something like CS50 existed, and offered for free by Harvard University. I discovered about this course from a random comment on some social media website. I always wanted to learn programming and tried learning from random courses/videos on the internet. But they all turned me off, and never learnt a single stuff. And as I discovered CS50, my life has completely changed. A year ago, I could hardly write a single line of code, let alone understand what it does under the hood. Now, I have built a full stack web application from scratch using a single framework. So I could only imagine how many people, who are passionate about computer programming, are missing out on pursuing this fantastic set of courses offered for free. Because when you google for "best programming course," the results you get on top are some random blogs that redirect you to some basic courses, but you will not find CS50 in any of those top results. 


Now, using SourceCrowd, people can search for whatever they want, and the order of results for webpages will not be decided by any kind of index, but based on the number of upvotes it received. Users can Upvote or Downvote a Source(links), based on whether it is helpful for searched term or not. So the order of results will be based on those votes. For example, there may be multiple sources with title "best programming course" which have a link to different pages like one may belong to Harvard's CS50 and other may lead to MIT's 6.0001. As people vote based on which they think is really the "best programming course," those sources will be on the top in search results. In short, this web app is a "decentralized web search index." Because the problem with search algorithms is it cannot decide whether the link results presented to the user based on their query has really helped them or not. Only a community can do that, and SourceCrowd fills that gap.


## Distinctiveness and Complexity:


The SourceCrowd project satisfies distinctiveness that we never created a search engine application during the coursework. And it is distinct from other projects in the course in the sense that we never implemented Upvote and Downvote button, which can increment or decrement the number of votes, though we just did like and unlike. This project also includes an official logo, which was created externally, and icons for upvote, downvote, save and delete, which we never explored in the coursework.


This project is also complex particularly due to the upvote and downvote feature, because upvote and downvote are separate buttons and when you click the one, the other is disabled. In order to change your preference of vote type, you will have to first undo the already chosen preference. There is also save(bookmark) button which saves the sources for the user and is accessible by visiting the saved route. And if the user wants to delete a source, they can do so by clicking the delete button which creates a popup modal, using dialog element, prompting user to confirm if they really want to delete the source or cancel. All these actions, including the checks for vote and save status when any route is visited, are achieved via the Fetch API routes, which requires complex functions in JavaScript. Another interesting feature I have implemented is that it tracks the number of people visited a particular link. It is not achieved via any API on clicking the link, but using an anchor tag attribute called "ping," which sends a post request to the app whenever somebody visits the link. Even the search has complexity because of the fact that it searches the queried term both in title and description of the source and deliver the results ordered by number of votes, making it easy for the user to find desired source.


## Files:


Static Folder : It contains the static files like JavaScript file, CSS File and other assets like the logos.


functions.js : It contains all the functions and Fetch APIs for voting, saving, and deleting the sources.


styles.css : It contains the stylesheet for all the html pages.


logo.png : It is image of the logo on index page.


mini.png : It is a mini logo, present in the header.


Templates Folder : it contains all the HTML pages, served from the backend based on the desired route.


layout.html : It is a HTML page which contains the important elements that are necessary to be present in all routes. The other HTML files are extended based on this page. It also contains the links to required sources to run the application like fonts, icons, stylesheet and JavaScript files.


login.html : It is a HTML file to be served when the login route is requested.


register.html : It is a HTML file to be served when the register route is requested.


index.html : It is a HTML file which is served when the index or home route is requested. It is default page of the application.


search.html : It is a HTML file which is served when the user searches for any query. It is served along with appropriate data from backend.


new.html : It is a HTML file to be served when then "new" route is requested, which serves all the sources sorted by the new.


saved.html : It is a HTML file for presenting the sources saved by the requested user.


profile.html : It is a HTML file for displaying the profile of requested user which includes all the sources created by them.


models.py : It contains all the models for creating, updating, deleting the data from database.


urls.py : It contains all the routes, including the APIs, which can be accessed by the users.


views.py : It contains the entire logic of the application, which decides what is to be served based on what is requested.


## How To Run Application:


1 . Make sure you are in the right directory which contains the appliction(capstone)


2 . Run the following command:


```
python manage.py runserver
```
