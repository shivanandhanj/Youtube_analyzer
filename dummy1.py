import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Clean the transcript to remove newline characters or other unwanted characters
def clean_transcript(text):
    return re.sub(r'\s+', ' ', text).strip()

# Retrieve relevant passages from the transcript
def retrieve_relevant_passages(transcript, question):
    # Split transcript into sentences or chunks for better processing
    documents = [transcript[i:i+1024] for i in range(0, len(transcript), 1024)]
    
    # Handle the edge case where there are no documents
    if not documents:
        return ""
    
    vectorizer = TfidfVectorizer().fit_transform(documents + [question])
    
    # Compute similarity between the question and each document
    similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1])
    
    # Get the top N most relevant passages, handle cases with fewer than 3 passages
    num_passages = min(3, len(documents))
    top_n_indices = similarities.argsort()[0][-num_passages:][::-1]
    relevant_passages = [documents[i] for i in top_n_indices]
    
    return ' '.join(relevant_passages)

# QA model using Hugging Face's pipeline for question-answering
qa_model = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')

def generate_answer(retrieved_passages, question):
    if not retrieved_passages:
        return "No relevant information found."

    # Use the QA model to generate the answer
    answer = qa_model(question=question, context=retrieved_passages)
    return answer['answer']

# Main function to ask a question and get an answer
def ask_question(transcript, question):
    # Clean the transcript and prepare it
    cleaned_transcript = clean_transcript(transcript)
    
    # Retrieve the most relevant parts of the transcript
    retrieved_passages = retrieve_relevant_passages(cleaned_transcript, question)
    
    # Generate the answer based on retrieved passages and question
    answer = generate_answer(retrieved_passages, question)
    
    return answer

# Example use case
transcript = """
"A web browser that runs inside the\nterminal. Why do we even need this? I don't know, but I want it. I\nwant to try it right now. Honestly, it sounds kind of awesome. I don't have\nto leave my terminal. I'm already there. It'll block ads by default because it\nlegit can't load them. I'm intrigued. How do you scroll and\nhow do you click links? I'm kind of excited to try that\nand yeah, I haven't set this up. So we're setting this up together.\nYou and me. Get your copy ready. This is five minute Friday. It's called links and the\nwebsite is kind of 1995. It's probably easy to browse with their\nbrowser. I get it. Oh wait, hold on. They have a version for Windows too.\nOkay, we're going to try that too. But first we'll do Linux\nseems pretty basic. On Debian, you're using a PT and then DNF\nof Fedora and Pacman on Arch. So I'm going to try this in Ubuntu on\nWSL. So curious about how this works. So we'll do a pseudo A PT install\nlinks. Do a dash y at the end, pseudo password. Let's\ngo. Okay, that was it. Now what I have no idea what to do,\nmaybe I just type in links. I'm using it. It's a fully featured worldwide web\nbrowser. They do have a user guide. I'm going to try and do\nthis without the user guide. So we use the up and down arrow keys\nto move, right to follow a link. Okay. And left to go back. That seems pretty\nsimple. I can get down with that. Okay, so I guess, hold on. What do I do?\nOkay, I think I'm at the main screen. I'm going to hit Oh, for options. What\nare my options here? You can do vi mode. This a little too much for me.\nLet's make my browser bigger here. I'm going to exit. Start it again.\nI just closed out of my Ubuntu. Okay, let's try it again. Oh, it was\nmade by the University of Kansas. That's pretty cool. Let's do\nquestion mark. I don't know, that's just searching stuff.\nOkay, we're on the main screen. If I type in G to go somewhere,\noh, there we go. So type in G. I'll go to network chuck.com.\nNow my site is very, very graphic heavy. It's going, oh my gosh, that's cool. Alright,\nso I'm just going to scroll down to, let's go to about the right arrow.\nYeah, it went to the About me page, which I need to update. It's\nonly got 2.8 million subscribers. I've got a lot more.\nAlright, go to academy. Now it's saying do I want to accept a\ncookie? I'm just going to put it always, man, this is so cool. I would not recommend going to academy\ndot number chuck.com with this because it's the video course website. So\nI think I've got the gist of this. Now how do I click on G again? Okay,\nso G will get you to another url. Let's try going to info dot\naci learning.com/network. Chuck, that's just a really terrible segue to\nour sponsor ACI learning the provider of IT pro. Okay, so this is\npretty cool. Now real quick, you do save 30% off your first\nmonth or year with code Chuck 30. Now what is it Pro? If you want to get\nstarted in it and learn things like, hey, what's a computer? All the way up to Linux and\nPowerShell on the cloud and hacking. You can do all that with IT Pro. You could start an entirely\nnew career with IT pro. They've got videos that\nwon't bore you to tears. We're going to try and get logged in.\nBrowsing this in a terminal is not easy. I love the description of the\nwhat, the fill in texts for photos, happy man in suit using\nlaptop. That could be you. I just want to get logged in platform\nlogins, choose my path ACI on demand, and that's where it dies because\nas we'll talk about later, it doesn't load things really well when\nyou have to use JavaScript and login forms or anything fancy. But seriously,\nhere's it pro the real website, much prettier. And again, they've got\neverything you need to get started. Entry level, it gets your A plus to\nnetwork plus security, plus CTNA. All the cloud certs. You have pretty\nmuch all of them. AWS certifications. They've got practice tests and\nthey've got virtual elapse. Pretty much everything you need to get\nstarted in it and prepare for practice exams. So again, check it out,\nlink below. Use a regular browser, not a terminal one for obvious reasons. And don't forget to use Chuck 30 for\n30% off your first month or year. Let's try. What would be a good\nwebsite? Go to bleeping computer. I got to admit that you accepting\nthe cookie thing every time is really annoying. This news\narticle is kind of crazy. National public data confirms breach\nexposing social security numbers. Let's go right Key to\nthat. One more cookies. Is there a way to always accept cookies?\nOh wait, am I saving a document? Cancel. This is so fun. Oh,\nI keep trying to go back and then I quit. Okay, that was so fun. Now I'm going to jump back in there\nand see if I can just enable, oh, I feel so out of my element with this. I'm going to go to options to see if I\ncan always accept cookies. Accept all. Okay, perfect. That'll make this\nso much better. And then, okay, so how do I get out and save? Oh, it's\nright here. Oh, shoot. Accept changes. There we go. You got to be\ncareful. You go to that left arrow, you're going to go back. Now they have a whole user\nguide of how to download stuff, navigating special links like\nmail tool links and comments. So kind of love this. But a couple of things because\nthis is a text-based only browser. You can't go to certain sites like\nYouTube and enjoy YouTube. Actually, I'm curious what happens when I\ngo to YouTube? We have to try it. Let's go to YouTube. Can I just type in A URL like this\nlinks and then I'll do youtube.com? Yes, it does it. I thought\nI told you. Oh, GPSI. That's cool. Okay, sure.\nYes. Accept all the cookies. Yeah, it hates this. So YouTube\nisn't going to work great. And any site that requires any kind\nof JavaScript or special scripts to allow you to log in like Gmail, it's\nnot going to do great with, but still, it's pretty fun. Let me know how you're going to use\nthis or if you'll ever use this. If anything, it's just fun to\ntry. Oh, and we forgot one thing. Can we install it on Windows? I don't\nknow why I'd want to because I've got WSL, but I'm curious. No, I'm\nnot going to mess with this. It's talking about Windows seven. I'm\nnot doing that. That's too old for me. I'll stick with Linux. Anyways, that's a five minute Friday fun little\ntool I found that could be fun for you. I'm not sure. I'll probably end up using\nit every once in a while. That's it. I'll catch you guys next time. shiva is a fucker"

...
"""

question = "who is shiva"

answer = ask_question(transcript, question)
print(answer)
