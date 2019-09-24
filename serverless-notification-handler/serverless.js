const path = require("path");
const { Component } = require("@serverless/core");

class ServerlessNotificationHandler extends Component {
  async default({ code, handler, env } = {}) {
    const snsTopic = await this.load("@serverless/aws-sns-topic");
    const snsSubscription = await this.load("@serverless/aws-sns-subscription");
    const lambda = await this.load("@serverless/aws-lambda");

    this.context.status(`Deploying Serverless Dashboard Notification handler`);

    const [snsTopicOutputs, lambdaOutputs] = await Promise.all([
      snsTopic({
        policy: {
          Version: "2008-10-17",
          Id: "policy_id",
          Statement: [
            {
              Action: ["SNS:Publish"],
              Sid: "statement_id",
              Effect: "Allow",
              Principal: { AWS: "arn:aws:iam::802587217904:root" },
              Condition: undefined
            }
          ]
        },
        displayName: "Serverless Alerts",
        name: "serverless-alerts"
      }),
      lambda({
        code: ".",
        name: "serverless-alert",
        env: {
          ...env,
          USER_HANDLER: handler
        },
        handler: "shim.sns",
        shims: [path.join(__dirname, "shim.py")],
        runtime: "python3.7",
        description:
          "Lambda for processing alerts from the Serverless Dashboard"
      })
    ]);

    const snsSubscriptionOutputs = await snsSubscription({
      topic: snsTopicOutputs.arn,
      endpoint: lambdaOutputs.arn,
      protocol: "lambda"
    });

    return { arn: snsTopicOutputs.arn };
  }

  async remove() {
    const snsTopic = await this.load("@serverless/aws-sns-topic");
    const snsSubscription = await this.load("@serverless/aws-sns-subscription");
    const lambda = await this.load("@serverless/aws-lambda");

    this.context.status(`Removing Serverless Dashboard Notification handler`);

    await snsSubscription.remove();
    await Promise.all([snsTopic.remove(), lambda.remove()]);
  }
}

module.exports = ServerlessNotificationHandler;
