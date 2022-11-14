import os
import json
import boto3
def lambda_handler(event, context):
    data = json.dumps(event["detail"])
    data_full = json.dumps(event)
    data_dic = json.loads(data)
    data_dic_full = json.loads(data_full)
    RESOURCE = data_dic_full["resources"]

    CHECK_TAG_LIST = ["Name", "AWSBackup"]
    SERVICE = data_dic["service"]
    CHANGE_TAG_KEYS = data_dic["changed-tag-keys"]
    RESOURCE_TYPE = data_dic["resource-type"]
    TAGS = data_dic["tags"]
    print(RESOURCE)
    print(SERVICE)
    print(CHANGE_TAG_KEYS)
    print(type(CHANGE_TAG_KEYS))
    print(RESOURCE_TYPE)
    print(TAGS)
    print(data_dic)
    # output=str("Service Change is %s, Resource Type is %s, Change Tag Key is %s, New Tag value is %s " % (SERVICE, RESOURCE_TYPE, CHANGE_TAG_KEYS, TAGS) )
    TAG_CHANGE_DETAIL = ''
    for k, v in TAGS.items():
        print(k, v)
        TAG_CHANGE_DETAIL += str("Change Tag Key: " + k + ", " + "New Tag value: " + v + " \n")
    SUBJECT="Resource %s Tag has been changed in AWS" % RESOURCE
    output=str("%s \nService Change is %s, Resource Type is %s \nTags have been updated to new value as below: \n%s" % (SUBJECT, SERVICE, RESOURCE_TYPE, TAG_CHANGE_DETAIL) )

    print(SUBJECT)
    s = set(CHECK_TAG_LIST) & set(CHANGE_TAG_KEYS)
    if len(s):
        print("Set is not empty, Tag change need to notify")
        try:
            client = boto3.client('sns')
            snsArn = 'arn:aws:sns:ap-southeast-1:123123:sc'

            response = client.publish(
                TopicArn = snsArn,
                Message = output ,
                Subject= "[Notification] Resource Tag has been changed in AWS"
            )
            print("Send successfully")
        except Exception as e:
            print(e)
            raise e
    else:
        print("Tag does not require to notify")

    

