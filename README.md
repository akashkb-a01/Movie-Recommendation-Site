<div id="top"></div>

<div align="center">

  <h1 align="center">Movie Recommendation Site</h1>

  <p align="center">
    An awesome movie recommendation site made using Django.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Creator</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project was developed for the `Engage 2022` program  for engineering students across India graduating in 2024.  
The topic I chose was to develop a recommendation engine by using the knowledge of algorithms.  

The major highlights of the projects are

* Login for existing users and Signup for new users.
* Recommending movies by filtering the adult content for kids users.
* Recommending movies by genre, directors, popularity, vote average ...
* Users can search for a movie.
* Users are able to add/remove movies to their list.
* Users are able to give ratings to a particular movie from which, they would be recommended movies based on the ratings of other users (`Collaborative filtering`)

Of course, no recommenation system is always accurate, so I have recommended movies by various parameters and also I plan to include more parameters in future developements.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

The web app is made with

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)
* HTML, CSS, JS

Django was preffered for the developement of the project due to the following reasons

* As, Django uses MVT architecture, so it offers rapid-developement.  
* Built in database support.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

For running the application on your local machine first clone the project repo using
* git clone
    ```sh
    git clone https://github.com/akashkb-a01/Movie-Recommendation-Site.git
    ```


### Installation

After cloning the repo to the machine, follow the follwing steps

Install the requirements for the project with
* pip 
    ```sh
    pip install -r requirements.txt
    ```

After installing the requirements, we are ready to run the website by entering the following command on the terminal
* python3
    ```
    python3 manage.py runserver
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Once the website is live, we can go to any browser and access the site by the following url
```
https://www.localhost:8000
```

After signing up/logging in, we can explore the functionalities the project has to offer.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
This section is for the future developement plans

- [] Email verification and forgot password option for users
- [] Add additional parameters for recommending movies
    - [] Keywords
    - [] Cast and Crew


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Creator

Akash Biswas - akashkb.a01@gmail.com

Project Link: [https://github.com/akashkb-a01/Movie-Recommendation-Site](https://github.com/akashkb-a01/Movie-Recommendation-Site)

<p align="right">(<a href="#top">back to top</a>)</p>


