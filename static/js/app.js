function setupDrop(dropId, inputId, previewId) {
  const drop = document.getElementById(dropId);
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);

  // click en drop abre input
  drop.addEventListener("click", () => input.click());

  // drag&drop
  drop.addEventListener("dragover", e => {
    e.preventDefault();
    drop.classList.add("dragover");
  });

  drop.addEventListener("dragleave", () => drop.classList.remove("dragover"));

  drop.addEventListener("drop", e => {
    e.preventDefault();
    drop.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      input.files = e.dataTransfer.files;
      showPreview(input, preview);
    }
  });

  // input normal
  input.addEventListener("change", () => showPreview(input, preview));
}

function showPreview(input, preview) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
}

// inicializamos
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("hideDrop")) {
    setupDrop("hideDrop", "hideInput", "hidePreview");
  }
  if (document.getElementById("revealDrop")) {
    setupDrop("revealDrop", "revealInput", "revealPreview");
  }
});
