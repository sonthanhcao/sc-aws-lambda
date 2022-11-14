# Python program to read
# json file
  
  
import json
  
with open('sample.json', 'r') as f:
  data = json.load(f)
  #data2 = data["detail"]
  SERVICE = data["detail"]["service"]

  RESOURCE = data["resources"]
  SERVICE = data["detail"]["service"]
  CHANGE_TAG_KEYS = data["detail"]["changed-tag-keys"]
  RESOURCE_TYPE = data["detail"]["resource-type"]
  TAGS = data["detail"]["tags"]
# Output: {'name': 'Bob', 'languages': ['English', 'French']}
CHECK_TAG_LIST = ["Name", "2"]
print(RESOURCE)
print(SERVICE)
print(24)
print(RESOURCE_TYPE)
print(TAGS)
s = set(CHECK_TAG_LIST) & set(CHANGE_TAG_KEYS)
# if len(s):
#     print("Set is not empty")
# else:
#     print("Set is empty")

TAG_CHANGE_DETAIL = ''
for k, v in TAGS.items():
    print(k, v)
    TAG_CHANGE_DETAIL += str("Key: " + k + ", " + "Value: " + v + " \n")

# for s in mylist:
#   endstring += s
print(TAG_CHANGE_DETAIL)
output=str("RESOURCE is %s Service Change is %s, Resource Type is %s \nTags have been updated to new value as below: \n%s" % (RESOURCE, SERVICE, RESOURCE_TYPE, TAG_CHANGE_DETAIL) )
print("XXXX")
print(output)
if len(s):
    print("Set is not empty, Tag change need to notify")
    try:
        # client = boto3.client('sns')
        # snsArn = 'arn:aws:sns:ap-southeast-1:065140405948:kidangel'
        output=str("Service Change is %s, Resource Type is %s, Change Tag Key is %s, New Tag value is %s " % (SERVICE, RESOURCE_TYPE, CHANGE_TAG_KEYS, TAGS) )
        print(output)
        # response = client.publish(
        #     TopicArn = snsArn,
        #     Message = output ,
        #     Subject='[Notification] Resource Tag has been changed in AWS'
        # )
        print("Send successfully")
    except Exception as e:
        print(e)
        raise e
else:
    print("Tag does not require to notify")