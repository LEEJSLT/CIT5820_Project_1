from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

# EXAMPLE OF DATA
# {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c', 
#  'payload': 
#    {'message': 'Ethereum test message', 
#     'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF', 
#     'platform': 'Ethereum'}}

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    sig = content['sig'] # get the signature information
    payload = content['payload'] # get the payload list

    message = payload['message'] # get the message from payload
    pk = payload['pk'] # get the public key from payload
    platform = payload['platform'] # get the platform from payload
    
    # Json data check - if keys do not match requirement
    # mainField = ['sig', 'payload']
    # for field in mainField:
    #     if field not in mainField.keys():
    #         return jsonify(False)

    # payloadField = ['message', 'pk', 'platform']
    # for field in payloadField:
    #     if field not in payloadField.keys():
    #         return jsonify(False)

    # Verifying an endpoint for verifying signatures
    payload = json.dumps(payload)

    #Check if signature is valid
    # check on Ethereum platform
    if platform == 'Ethereum':
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        
        if eth_account.Account.recover_message(eth_encoded_msg, signature=sig) == pk:
            result = True
        else:
            result = False
    # check on Algorand platform
    if platform == 'Algorand':
        if algosdk.util.verify_bytes(payload.encode('utf-8'), sig, pk):
            result = True
        else:
            result = False
            
    # result = True #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
