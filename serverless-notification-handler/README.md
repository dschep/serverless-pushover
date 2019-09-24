# serverless-notification-handler

&nbsp;

Easily deploy a Python handler for handling Serverless Insight Alert Notifications.

&nbsp;

1. [Install](#1-install)
2. [Create](#2-create)
3. [Configure](#3-configure)
4. [Deploy](#4-deploy)

&nbsp;


### 1. Install

```console
$ npm install -g serverless
```

### 2. Create

```console
$ mkdir notification-forwarder && cd notification-forwarder
```

The directory should look something like this:


```
|- handler.py
|- serverless.yml
|- .env         # your AWS api keys
```

the `.env` file should look like this

```
AWS_ACCESS_KEY_ID=XXX
AWS_SECRET_ACCESS_KEY=XXX
```

The `handler.py` file should contain a function to handle a alert notification event from
Serverless Insights.

```python
def alert(notification):
    print('got notification', notification)
```

### 3. Configure

Configure your `serverless.yml` as follows:

```yml
# serverless.yml

name: notification-handler
stage: dev

notificationHandler:
  component: './serverless-notification-handler'
  inputs:
    code: .
    handler: handler.alert
    env:
      FOOBAR: ${env.FOOBAR} # Optional, set any env vars for your code
mySchedule:
  component: "@serverless/schedule"
```

### 4. Deploy

```console
$ serverless
```

### 5. Configure the Serverless Dashboard

Paste the ARN printed in the output of the previous step into the SNS notification configuration on
dashboard.serverless.com for your app.

&nbsp;

### New to Components?

Checkout the [Serverless Components](https://github.com/serverless/components) repo for more information.

