document.addEventListener("DOMContentLoaded", function () {
  const uploadSection = document.getElementById("upload");
  const ctaButton = document.querySelector(".cta-button");

  if (ctaButton && uploadSection) {
    ctaButton.addEventListener("click", function (e) {
      e.preventDefault();
      uploadSection.scrollIntoView({ behavior: "smooth" });
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const uploadSection = document.getElementById("upload");
  const ctaButton = document.querySelector(".cta-button");
  const resultSection = document.querySelector(".result-section");

  if (ctaButton && uploadSection) {
    ctaButton.addEventListener("click", function (e) {
      e.preventDefault();
      uploadSection.scrollIntoView({ behavior: "smooth" });
    });
  }

  if (resultSection) {
    resultSection.scrollIntoView({ behavior: "smooth" });
  }
});
