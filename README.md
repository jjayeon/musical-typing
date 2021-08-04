# ToneType

Do you like typing?  Do you like musical tones?  Then this is the place for you!  ToneType is a website where you can practice typing to the tune of delightful MIDI synthesizers.  Currently under construction.

## Installation

After cloning this repo, run the `install_docker.sh` script as root to set up Docker on your machine.  (Script is buggy.  May need some troubleshooting.)  If Docker is already installed, ignore this step.  Then, run `systemctl start docker` and `docker-compose up -d` to launch the app.

## Usage

The app should be accessible locally at `localhost:5000`, bypassing the SSL cert stuff.  As for production, the app as written expects to be running on the domain `tonetype.tech`; if it's not, the SSL cert/nginx container will almost certainly raise a problem.  If you're someone other than an MLH fellow assigned to work on this project, please fork, configure, and hack to your heart's content.

## A Beginner's Guide to Flask

[Flask](https://flask.palletsprojects.com/en/2.0.x/quickstart/) is a micro web framework written in Python.  The idea behind Flask is to convert HTTP requests into function calls Python can understand; this is accomplished through the use of `routes`, as in [our init file](app/__init__.py):

```python
@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))
```

The above code translates as follows: when we receive a request with the URL '/', give the user the HTML resulting from the `render_template()` call.

`render_template()` is a function that takes a template (`'index.html'`), some arguments to the template (`title="MLH Fellow", url=os.getenv("URL")`), and returns a complete HTML file.  The "template" in question is a [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) template, which basically lets you insert `{{ variables }}` into an a reusable HTML template.  (Other features and file formats are supported as well.)  You can check out [this repo's index page](app/templates/blog.html) for an example.

## Contributing

Pull requests are expected from certain MLH teammates; others will probably be ignored.  If you want to use this project for your own purposes, feel free to do so independently of our team, license permitting.
