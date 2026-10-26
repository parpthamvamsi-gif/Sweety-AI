async function talkToSweety() {
    let userInput = document.getElementById("userInput").value;
    let output = document.getElementById("output");
    
    if(!userInput) {
        output.innerText = "Sir, edaina adagandi please!";
        return;
    }
    
    output.innerText = "Chedhama Sweety: Thinking, Sir...";
    
    "IkkaAQ.Ab8RN6JLc_9ogkz8O37vnOBVaIYbf9ooLZdD19M9G2GKxyQi0A"
  da API key and request logic connect avthundi
    try {
        let response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=NEE_API_KEY_ICKADA_IVVU`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{ parts: [{ text: `You are Chedhama Sweety, a helpful AI assistant. Always address the user respectfully as 'Sir'. User query: ${userInput}` }] }]
            })
        });
        
        let data = await response.json();
        let reply = data.candidates[0].content.parts[0].text;
        output.innerText = "Chedhama Sweety: " + reply;
    } catch (error) {
        output.innerText = "Error, Sir: " + error.message;
    }
}
