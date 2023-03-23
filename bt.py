from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

openai.api_key = "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"
model_engine = "gpt-3.5-turbo" 
first_call_to_API = True

app = Flask(__name__)

 
@app.route("/", methods=["POST"])
# chatbot logic
def bot():	
	
	# user input
    # TODO: Twillio API 
    user_msg = request.values.get('Body', '').lower()

    gpt_model_context = '''Hello! You are a habit coach and productivity expert with years of experience on human behaviour and 
            psychology, I want you to act as a habit accountability partner for me, and help me make good habits and break the bad ones. Please provide 
            me with practical solutions & act as an accountablity partner in my journey, Kindly keep response less than 200 words, and try to provide 
            lists, headings, sections wherever you feel is required. If anyone asks questions besides this, please simply reply that you don't have enough information 
            of that topic, and reiterate that you can help with habit related questions.'''

    message = [{"role": "user", "content": user_msg}]

    global first_call_to_API
    if first_call_to_API is True:
        message = [{"role": "system", "content": gpt_model_context}, {"role": "user", "content": user_msg}],
        first_call_to_API = False

	# response from chat-gpt
    chat_gpt_response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages = message
    )


    chat_gpt_message = chat_gpt_response.choices[0]['message']    	
        
    # creating object of MessagingResponse
    response = MessagingResponse()

    # url to pdf
    url = "https://www.africau.edu/images/default/sample.pdf"

    # check for specific user message
    try: 
        if chat_gpt_message['role'] == 'assistant':
            gpt_reply_msg = response.message(chat_gpt_message['content'])

            if(first_call_to_API):
                print(print("################################ \n {}: {} \n\n ################################".format("System Context", gpt_model_context)))

            print("{}: {} \n".format("user", user_msg))
            print("{}: {} \n".format(chat_gpt_message['role'], chat_gpt_message['content']))      
            # TODO: backup in txt file
    except:
        raise Exception

    return str(response)
 
 
if __name__ == "__main__":
    app.run(port=5100)

