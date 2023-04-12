
// Replace 'your_server_ip' with the actual IP address of your Vultr server
const apiUrl = "https://api.rankmytweets.com/generate"; // Update this with the correct API URL

// Function to make an API request and receive generated text
async function getGeneratedText(tweetContent) {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_text: tweetContent }),
    });

    const data = await response.json();
    console.log("API response:", data); // Add console log here
    return data.generated_text;
  } catch (error) {
    console.error("Error while fetching generated text:", error);
  }
}

document.getElementById("submitTweet").addEventListener("click", async () => {
  const tweetContent = document.getElementById("tweetContent").value;
  const generatedText = await getGeneratedText(tweetContent);
  console.log("Generated text:", generatedText); // Add console log here

  const revisedTweetsContainer = document.getElementById("revisedTweets");

  if (generatedText) {
    revisedTweetsContainer.innerHTML = `
      <h3>Revised Tweet:</h3>
      <pre>${generatedText}</pre>
    `;
  } else {
    revisedTweetsContainer.innerHTML = `
      <h3>Revised Tweet:</h3>
      <p>Failed to fetch revised tweet. Please try again later.</p>
    `;
  }
});
