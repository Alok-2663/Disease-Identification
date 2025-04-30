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
        success: function(response) {
            $('#result').html(
                "<strong>Model Prediction:</strong> " + response.prediction +
                "<br><strong>Confidence Level:</strong> " + (response.confidence * 100).toFixed(2) + "%"
            );
            $('#result-container').fadeIn();
        },
        error: function(xhr, status, error) {
            $('#result').html("❌ <strong>Error:</strong> " + error);
            $('#result-container').fadeIn();
        }
    });
}

// Add event listeners after page is loaded
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("fileInput").addEventListener("change", previewImage);

    // Fix: Make sure upload button has id="uploadButton"
    document.querySelector("button[onclick='uploadImage()']").setAttribute("id", "uploadButton");

    document.getElementById("uploadButton").addEventListener("click", uploadImage);
});
