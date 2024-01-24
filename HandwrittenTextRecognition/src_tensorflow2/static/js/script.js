const filePicker = document.getElementById("file-picker");
const detectBtn = document.getElementById("detect-button");
const errorMsg = document.getElementById("error-msg");
const resMsg = document.getElementById("res-msg");
detectBtn.disabled = true;

$(document).ready(function () {
    filePicker.addEventListener("change", () => {
        const files = filePicker.files;

        if (
            !Array.from(files).every((image) => {
                return /text.*/.test(image.type);
            })
        ) {
            errorMsg.textContent = "All files must be in .txt format!!";
            detectBtn.disabled = true;
            return;
        }

        if (files.length > 1) {
            detectBtn.disabled = false;
        } else {
            console.log("Select more than 2 files!!");
            errorMsg.textContent = "Select more than 2 files!!";
            detectBtn.disabled = true;
        }
    });

    detectBtn?.addEventListener("click", async function () {
        event.preventDefault();

        showLoadingSpinner();
        const form = document.getElementById("detector-form");
        const formData = new FormData(form);
        const response = await fetch("detect-plagiarism", {
            method: "POST",
            body: formData,
        });

        res = await response.text()

        lines = res.split('\n')

        res = lines.join(' <br> ')

        resMsg.innerHTML = res
        hideLoadingSpinner();
    });
});

function showLoadingSpinner() {
    $("#loadingSpinner").show();
    detectBtn.disabled = true;
}

function hideLoadingSpinner() {
    $("#loadingSpinner").hide();
    detectBtn.disabled = false;
}
