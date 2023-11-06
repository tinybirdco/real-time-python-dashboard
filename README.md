# Build a real-time dashboard in Python with Tinybird and Dash

Use this repository to build a real-time dashboard in Python using Tinybird and Dash. To learn more about this implementation, check out the [blog post](https://www.tinybird.co/blog-posts/python-real-time-dashboard).

## 0. Prerequisites

To implement this project, you'll need to have the following installed

- Python > v3.8
- Node.js > v18 (to use the Mockingbird CLI)

## 1. Get started

Clone the repository:

```bash
git clone https://github.com/tinybirdco/real-time-python-dashboard.git
cd real-time-python-dashboard
```

Setup virtual environment:

```bash
python -mvenv .e
. .e/bin/activate
echo ".e*" >> .gitignore
```

Install requirements:

```bash
pip install requirements.txt
```

Install Tinybird CLI

```bash
pip install tinybird-cli
```

## 2. Create a Tinybird Workspace

If you need a free Tinybird account, [sign up here](https://www.tinybird.co/signup).

Go to [ui.tinybird.co](https://ui.tinybird.co) and create a Workspace called in either region. Copy your user admin token from the Tokens in the UI. This is the token associated to your email address:

![image](/img/token.jpg)

## 3. Authenticate to Tinybird

Authenticate to your Tinybird Workspace

```bash
cd data-project
tb auth --token <your user admin token>
echo ".tinyb" >> .gitignore
```

## 4. Push Tinybird resources

From the `data-project` folder, run the following to push the Tinybird Pipes and Data Source to your Workspace:

```bash
tb push datasources pipes
```

## 5. Stream data to Tinybird

For this demo, you'll use Mockingbird to stream mock data to Tinybird to populate your `flight_bookings` Data Source with mock flight bookings data.

### Install the Mockingbird CLI

```bash
npm install -G @tinybirdco/mockingbird-cli
echo "node_modules" >> .gitignore
```

### Start streaming

You can send up to 1,000 rows per second to Tinybird using Mockingbird:

```bash
export TB_HOST=<us_gcp OR eu_gcp>
export TB_TOKEN=<your_user_admin_token>
mockingbird-cli tinybird \
--template "Flight Bookings" \
--eps 10  \
--endpoint=$TB_HOST \
--datasource=flight_bookings \
--token=$TB_TOKEN
```

## 6. Run the dashboard

From the main project directory:

```bash
python app.py
```

Open [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view your real-time dashboard.

![image](/img/dashboard.png)

## Contributing

If you find any issues or have suggestions for improvements, please submit an issue or a [pull request](https://github.com/tinybirdco/real-time-python-dashboard/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc).

## License

This code is available under the MIT license. See the [LICENSE](https://github.com/tinybirdco/real-time-python-dashboard/blob/main/LICENSE.txt) file for more details.

## Need help?

&bull; [Community Slack](https://www.tinybird.co/join-our-slack-community) &bull; [Tinybird Docs](https://docs.tinybird.co/) &bull;

## Authors

- [Cameron Archer](https://github.com/tb-peregrine)
