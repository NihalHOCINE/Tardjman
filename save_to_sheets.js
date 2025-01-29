
// JavaScript function to handle feedback
function handleFeedback(rating) {
    const inputText = document.getElementById("input-text").value;
    const outputText = document.querySelector("#output-text p").innerText.replace("الترجمة: ", "");

    // Prepare the data
    const data = {
        input_sentence: inputText,
        output_sentence: outputText,
        rating: rating, // 1 for like, 0 for dislike
    };

    // Send feedback to google sheet
    const url = "https://script.google.com/macros/s/AKfycbwXhrRfSPRj6c66WWZPH9FzNNM9L-N5f2kbF7GAU9BoBOgbhDpIgk5b6HuBp6s3JSoc/exec"; // Replace with your Web App URL

    fetch(url, {
        method: 'POST',
        mode: 'no-cors', // Use 'no-cors' for now, but ideally use proper CORS setup
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
    alert("شكرًا على تقييمك!");
        } else {
    alert("حدث خطأ أثناء حفظ التقييم.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("حدث خطأ أثناء حفظ التقييم.");
    });
}