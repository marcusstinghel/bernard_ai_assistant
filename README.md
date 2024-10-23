# Bernard AI Assistant

---
This project uses an algorithm, located in the kernel package, to respond to customer inquiries and requests for
Octapipe, integrating with the ChatGPT API. The algorithm interprets the natural language of the questions, matches them
with predefined queries, and securely executes the necessary SQL queries to generate a response based on that data.
Additionally, the project includes an API to receive customer inquiries, send the question history, and collect feedback
on response quality.

---

## Bernard Web API

### Create message

This endpoint uses the POST method to receive the customer's inquiry and return a response with the retrieved data.

cURL:

```bash
curl --location 'https://bernard.octapipe.com/messages' \
--header 'Content-Type: application/json' \
--data '{
    "question": "User question",
    "customer_uuid": "5039a4f7-f539-48c0-b8f4-c6af1db444df",
    "user_uuid": "042a2815-51fd-45c0-9391-d5f5bd50c474"
}'
```

### Read messages

This endpoint uses the GET method to retrieve the user's message history.

cURL:

```bash
curl --location 'https://bernard.octapipe.com/messages?customer_uuid=5039a4f7-f539-48c0-b8f4-c6af1db444df&user_uuid=042a2815-51fd-45c0-9391-d5f5bd50c474'
```

### Update message

This endpoint uses the PUT method to submit feedback indicating whether the response was helpful or not for the
customer.

cURL:

```bash
curl --location --request PUT 'https://bernard.octapipe.com/messages' \
--header 'Content-Type: application/json' \
--data '{
    "message_uuid": "39d70c59-1ee5-4e1e-a5d3-c68a9afd347c",
    "is_solved": false
}'
```

---

## Bernard Kernel

The kernel of the project is located in the `kernel` package, in the `kernel.py` file, and is implemented in
the `Kernel` class. In the constructor function `__init__`, the communication with the ChatGPT API is initialized, along
with the communication with the project and Octapipe databases.

### Project Logic:

The project's logic consists of:

1. **Defining the Entity and Context of the Question**: Understanding what the customer is asking.
2. **Relating to the Predefined Question**: Identifying the inquiry that most closely resembles the customer's question
   or informing if the question is not supported.
3. **Dynamically Building the Query**: Creating the necessary query to retrieve relevant data for the response.
4. **Constructing the Response**: Generating an appropriate answer based on the obtained data.
5. **Recording the Message in the Database**: Storing the interaction in the database for future history and analysis.

The main function, `respond`, is the only public function of the class and is responsible for all the abstract logic of
the algorithm, managing the processing of customer inquiries and generating the appropriate responses.

---

## Bernard Database

The project utilizes the following tables to manage interactions and ensure security and efficiency in data extraction:

### 1. Messages

The `messages` table stores a record of all customer inquiries, the responses provided, and reviews of those responses.
This table is essential for maintaining a history of interactions and allowing for performance analysis of the system,
as well as providing insights into the most frequently asked questions by users.

### 2. Questions

The `questions` table contains all predefined inquiries, ensuring security in data extraction. This table can be
continuously updated and populated to expand the system's response capabilities, making the project more robust and able
to handle a wider variety of questions.

### 3. Prompts

The `prompts` table stores all necessary prompts for conducting communications and requests made to the ChatGPT. These
prompts are crucial for ensuring that interactions with the API are accurate and effective, leading to a better user
experience.

---

## Octapipe Database

The communication with the Octapipe database is solely for extracting the necessary data to inform responses to
customers. This approach ensures that interactions are secure and efficient, allowing the system to provide accurate and
relevant information in response to user inquiries.
