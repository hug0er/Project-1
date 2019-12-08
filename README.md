# Project 1

This project consists on the implementation of a book review page. To better explain this project, we can divide it into 3 components that are: authentication, book search, and reviews.

- The first component Corresponding to the authentication, uses** index.html** to display a page on which the user can enter with his account data (username and password), in case he does not have an account, the user can click the hyperlink to redirect to **register_form.html** and create an account with a new username. If the username chooses by the user is occupied, it is redirected to **no_success.html**, where the message of that the username is taken appears, and he can go back to **index.html**, or **register_form.html**. If he chooses to log in and his username or password fails, **error_pass.html** is rendered, showing the error. In case there is no error, the user will be redirected to** search.html**.

- For the book search (** search.html**), the user has an input field to search the book by ISBN, title or author. In this case, the user must press enter to start the search, we do not use a button for aesthetic reasons. Once the search has been carried out if there are results, all those that comply with the search are presented, if there are no results, a message is displayed. In the list of book results, the user can click on them to be redirected to **books.html**. Where the information of the selected book will be presented, in addition to its reviews created through the page and the ones of the Goodreads API.  At this point the user can logout, to be redirected to **index.html**, return to **search.html** or go to **review.html**.

- Finally, review.html contains input fields, that are going to receive a review. If the user already reviews the current book, the review is updated and the user is sent to review-update.html, if the review is new the user is redirected to review-new.html, where the user can logout or return to search.html.

**Note:** To obtain the **API** the user should visit *url/api/"ISBN number”*, if the book does not exist, an error message appears. The values to be set in order to run the environment are:

- set FLASK_APP=application.py

- set DATABASE_URL=postgres://trgzqcnracvcxr:95c3dc26df8688c7e8f94401454c25dce83a94a5c19c0f3bba4694b7643c0db0@ec2-54-235-104-136.compute-1.amazonaws.com:5432/d40b302ipd1hj5
