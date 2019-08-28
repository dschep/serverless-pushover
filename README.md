# ⚡📲 Serverless Pushover

A Serverless project that forwards webhook notifications from
[Serverless Dashboard](https://dashboard.serverless.com)
to [Pushover](https://pushover.net).

![Screenshots of a push notification and detail in Pushover](./screenshots.png)


## Setup instructions
1. Clone this repo & `cd` into it
   ```shell
   git clone https://github.com/dschep/serverless-pushover
   cd serverless-pushover
   ```
1. Install the serverless framework
   ```shell
   npm i -g serverless
   ```
1. Create a new application on pushover by clicking [this link](https://pushover.net/apps/build)
1. Deploy! Replace `<USER>` and `<APP>` with your Pushover user key and the
   key/token for the app you just created respectively.
   ```shell
   PUSHOVER_USER_KEY=<USER> PUSHOVER_APP_KEY=<APP> serverless deploy
   ```
1. Use the URL for your endpoint from the deploy output in a webhook notification
   configuration on [dashboard.serverless.com](https://dashboard.serverless.com)
