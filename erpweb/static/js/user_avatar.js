document.addEventListener("DOMContentLoaded", function () {
    // Open file picker
    document.querySelectorAll(".btn-avatar-change").forEach(button => {
        button.addEventListener("click", function () {
            this.closest(".modal-body").querySelector(".avatar-input").click();
        });
    });

    // Remove avatar
    document.querySelectorAll(".btn-avatar-remove").forEach(button => {
        button.addEventListener("click", function () {
            const modalBody = this.closest(".modal-body");
            modalBody.querySelector(".avatar-preview").src = "/static/img/avatar.png";
            modalBody.querySelector(".avatar-input").value = "";
            modalBody.querySelector(".avatar-remove-flag").value = "true";
        });
    });

    // Preview selected file
    document.querySelectorAll(".avatar-input").forEach(input => {
        input.addEventListener("change", function () {
            const file = this.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = e => {
                this.closest(".modal-body").querySelector(".avatar-preview").src = e.target.result;
                this.closest(".modal-body").querySelector(".avatar-remove-flag").value = "";
            };
            reader.readAsDataURL(file);
        });
    });
});
