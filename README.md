## An opensource chat service that cares about your privacy.

![blackPigeon](https://user-images.githubusercontent.com/80196658/142221311-9f9c136b-0c93-4241-be09-5fd96fd7dc89.gif)


## Instructions to set up a local testing environment:


#### 1) Clone this repository and navigate to its root directory

#### 2) Create a python virtual environment called 'my_env'

```
$ python3 -m venv my_env
```
#### 3) Activate the virtual environment:

```
$ source ./my_env/bin/activate
```

##### (You should notice that the console starts displating the virtual environment's name before your own and the dollar-sign).



#### 4) Install this app's dependencies on the virtual environment you just created:

```
(my_env)$ pip install -r requirements.txt
```
#### 5) Run the app on localhost:

```
(my_env)$ python3 -m flask run
```

#### Example output:

```
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

#### Click on the link, and the main page will be launched on your default browser. Yay!





