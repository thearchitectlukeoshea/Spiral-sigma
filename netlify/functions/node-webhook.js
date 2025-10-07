exports.handler = async function(event, context) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    const data = JSON.parse(event.body);
    console.log("Received data from Colab node:", data);

    // TEMP: echo back for now. Later, store in Render DB or JSON file.
    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Update received successfully!" })
    };
  } catch (error) {
    console.error("Error processing webhook:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Error processing update." })
    };
  }
};
