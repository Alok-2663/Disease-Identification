// Function to preview selected image
function previewImage() {
    $('#result-container').hide(); // Hide result on new selection
    var file = document.getElementById("fileInput").files[0];

    if (file) {
        var reader = new FileReader();
        reader.onload = function(event) {
            var imgElement = document.getElementById("preview");
            imgElement.src = event.target.result;
            imgElement.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
}

// Function to upload image using AJAX
function uploadImage() {
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput').files[0];

    if (!fileInput) {
        alert("Please select an image to upload.");
        return;
    }

    formData.append("file", fileInput);

    $.ajax({
        url: '/predict',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json', // ensures jQuery tries to parse JSON
        success: function(response) {
            if (response && response.prediction && response.confidence !== undefined) {
                $('#result').html(
                    "<strong>Model Prediction:</strong> " + response.prediction +
                    "<br><strong>Confidence Level:</strong> " + (response.confidence * 100).toFixed(2) + "%"
                );
            } else {
                $('#result').html("⚠️ <strong>Unexpected response format.</strong>");
            }
            $('#result-container').fadeIn();
        },
        error: function(xhr, status, error) {
            let errorMessage = "❌ <strong>Error:</strong> " + error;
            if (xhr.responseText) {
                errorMessage += "<br><em>Details:</em> " + xhr.responseText;
            }
            $('#result').html(errorMessage);
            $('#result-container').fadeIn();
        }
    });
}

// Add event listeners after page is loaded
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("fileInput").addEventListener("change", previewImage);

    const uploadBtn = document.querySelector("button[onclick='uploadImage()']");
    if (uploadBtn) {
        uploadBtn.setAttribute("id", "uploadButton");
        document.getElementById("uploadButton").addEventListener("click", uploadImage);
    }
});
