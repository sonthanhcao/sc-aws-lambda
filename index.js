// Load the SDK for JavaScript
var AWS = require('aws-sdk');
// Set the region
AWS.config.update({region: 'eu-central-1'});
// Create EC2 service object
ec2 = new AWS.EC2({apiVersion: '2016-11-15'});

exports.handler = (event, context, callback) => {
  var detail = event.detail

  // no action if this event is not about ec2 instance
  if (!(detail["service"] === "ec2" && detail["resource-type"] === "instance")) return

  var tags = detail["tags"]

  console.log(tags)

  // if associated tags not contain the expected tag pair
  if (!tags.hasOwnProperty("valid-key") || tags["valid-key"] !== "valid-value"){
    console.log("This is an invalid instance.")

    var resourceSplit = event.resources[0].split("/")
    var params = {
      InstanceIds: [resourceSplit[resourceSplit.length - 1]], // extract the last part of resource name as instance id
      DryRun: true
    };

    // call EC2 to stop the selected instances
    ec2.stopInstances(params, function(err, data) {
      if (err && err.code === 'DryRunOperation') {
        params.DryRun = false;
        ec2.stopInstances(params, function(err, data) {
          if (err) {
            callback(err, "fail");
          } else if (data) {
            console.log("Success", data.StoppingInstances);
            callback(null, "Success");
          }
        });
      } else {
        callback(err)
      }
    });
  } else {
    console.log("This is a good instance.")
    callback(null, "no action");
  }
};