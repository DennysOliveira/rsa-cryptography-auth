# RSA Cryptography Authentication Proof-of-Concept
![GitHub Repo size](https://img.shields.io/github/repo-size/bardsnight/aps-proj?style=flat-square)
![GitHub Languages](https://img.shields.io/github/languages/count/bardsnight/aps-proj?style=flat-square)
![GitHub Issues](https://img.shields.io/github/issues/bardsnight/aps-proj?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/bardsnight/aps-proj?style=flat-square)
![License](https://img.shields.io/github/license/bardsnight/aps-proj?style=flat-square)
> This project was a request by Structured Programming lectures in Computer Science college.
> <br>It runs with both a Python front-end CLI structure and API Endpoints running with Flask.

<!--ts-->
   * [Features](#Features)
   * [Requirements](#Requirements)
   * [Installation](#Installation)
   * [Usage](#Usage)
   * [Dependencies](#Dependencies)
   * [Contributors](#Contributors)     
   * [License](#License)   
<!--te-->

## Features
This application does feature a simple authentication concept with encryption over the data transfered between the client and the endpoint.<br>
- [x] User registration
- [x] User authentication
 
## Requirements
* Python `v3.0` or greater is required.
* This project was tested only in `Windows`. Might be able to run it on `Linux` and other *nix based operational systems.

## Installation
#### Windows:
- First, clone this repository or download the folder and extract it somewhere
<br>`$ git clone https://github.com/bardsnight/aps-proj.git`

- Create a python virtual environment
<br>`$ python -m venv venv`

- Activate the virtual environment
<br>`$ .\venv\Scripts\activate`

- Install project dependencies
<br>`$ pip install -r requirements.txt`

## Usage
This application is deployed with both the client `main.py` and the Flask API `app.py`.
You have to run both to be able to reproduce the concept.

- First, run the Flask API with the Virtual Environment (venv) active:<br>
`$ (venv) $ flask run`<br>
By default, **flask run** will run **app.py**.


Your API should now be running at `http://localhost:500/`.<br>


- Open up another CLI and run the main application:<br>
`(venv) $ python .\main.py`


**You can now select whichever options you wanna test.**<br>
1 for logging in with a existent user.<br>
2 for registering a new user.<br>
3 to quit the application.<br>


## Dependencies
This application was developed with help of the following Python packages and its subdependencies:
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [RSA](https://stuvel.eu/software/rsa/)

Also, some other tools were used during the development process:
- [Insomnia](https://insomnia.rest/)
- [SQLite Studio](https://sqlitestudio.pl/)


## Contributors
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/blacklebe#">
        <img src="https://avatars.githubusercontent.com/u/92761332?v=4" width="100px;" alt="Contributor Avatar on GitHub"/><br>
        <sub>
          <b>Calebe</b>
        </sub>
      </a>
    </td>    
  </tr>
</table>


## Author
<a href="https://github.com/bardsnight/">
<img style="border-radius: 5px;" src="https://avatars.githubusercontent.com/u/51341598?s=400&u=9431c2dc6cbc497de03fdda80330fcc45a9c4fa9&v=4" width="70px" alt="Author Profile Picture"/>
<br><b>Dennys Marcos</b>
</a>

Made with lots of ☕.

[![Linkedin Badge](https://img.shields.io/badge/Linkedin-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dennysm/)
[![Mail Badge](https://img.shields.io/badge/ProtonMail-8B89CC?style=flat&logo=protonmail&logoColor=white)](mailto:dennysm@pm.me)

## License
This project is licensed under the terms of the MIT license. Check the file [license](LICENSE) for deteails.

[⬆ Go to the top](#RSA-cryptography-authentication-Proof-of-Concept)