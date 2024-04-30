# Social Network Project
This repository contains the codebase for a social networking application built with Django. The application allows users to make posts, follow/unfollow other users, like posts, and navigate through paginated lists of posts.

## Features
- User Authentication: Users can register, log in, and log out.
- Making Posts: Authenticated users can create posts with a character limit.
- Editing Posts: Users can edit their own posts.
- Liking Posts: Users can like and unlike posts.
- Following: Users can follow and unfollow other users.
- Pagination: Posts are displayed with pagination support.
## Key Files and Directories
- network/templates/network/: Contains HTML templates for the application views.
- make_post.html: Template for creating a new post.
- index.html: Main page showing all posts.
- following.html: Shows posts from followed users.
- profile.html: User profile page showing user's posts and follow/unfollow button.
- edit_post.html: Template for editing an existing post.
- register.html: Registration page for new users.
- network/static/network/: Contains static files like CSS and JavaScript.
- network.js: JavaScript for handling likes and other dynamic features.
- project4/settings.py: Django project settings.
- TEMPLATES: Configuration for Django templates.
## Setup and Installation
- Clone the repository:

- git clone https://github.com/lolocompa/network.git
- cd network
- Install the required dependencies:

- pip install -r requirements.txt
- Apply the migrations:

- python manage.py migrate
- Run the development server:

- python manage.py runserver
- Visit http://127.0.0.1:8000/ in your web browser to start using the application.

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is open-source and available under the MIT License.
