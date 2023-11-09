$(function () {
  //search
  $(document).on("keydown", (e) => {
    switch (e.key) {
      case "k":
      case "Control":
        e.preventDefault();
        e.stopPropagation();
        break;
    }
    ``;
    if (e.key === "k" && e.ctrlKey) {
      $("#search").trigger("focus");
    }
  });
  //drawer
  $(".drawer-btn").on("click", () => {
    const checkClassExits = $(".layout-wrapper");
    if (checkClassExits.hasClass("active")) {
      checkClassExits.removeClass("active");
    } else {
      checkClassExits.addClass("active");
    }
  });
  //drawer key access
  $(document).on("keydown", (e) => {
    switch (e.key) {
      case "b":
      case "Control":
        e.preventDefault();
        e.stopPropagation();
        break;
    }
    if (e.key === "b" && e.ctrlKey) {
      const checkClassExits = $(".layout-wrapper");
      if (checkClassExits.hasClass("active")) {
        checkClassExits.removeClass("active");
      } else {
        checkClassExits.addClass("active");
      }
    }
  });
});

///Editor
function QuillIsExists() {
  const editorOne = document.querySelector("#editor");
  const editorTwo = document.querySelector("#editor2");
  var toolbarOptions = [
    [{ header: [1, 2, 3, 4, 5, 6, false] }],
    ["bold", "italic", "underline"], // toggled buttons
    [{ list: "ordered" }, { list: "bullet" }],
    ["link", "image"],
  ];
  if (editorOne) {
    var editor = new Quill("#editor", {
      modules: {
        toolbar: toolbarOptions,
      },
      theme: "snow",
    });
  } else if (editorTwo) {
    let editorTwo = new Quill("#editor2", {
      modules: {
        toolbar: "#toolbar2",
      },
      theme: "snow",
    });
  } else {
    return false;
  }
}
QuillIsExists();

// Settings Tab
const tabs = document.querySelectorAll(".tab");
const tabContent = document.querySelectorAll(".tab-pane");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.getAttribute("data-tab");

    tabs.forEach((tab) => {
      tab.classList.remove("active");
    });
    tab.classList.add("active");

    tabContent.forEach((content) => {
      if (content.getAttribute("id") === target) {
        content.classList.add("active");
      } else {
        content.classList.remove("active");
      }
    });
  });
});

//Faq
const accordionHeader = document.querySelectorAll(".accordion-header");
accordionHeader.forEach((header) => {
  header.addEventListener("click", function () {
    const accordionContent =
      header.parentElement.querySelector(".accordion-content");
    let accordionMaxHeight = accordionContent.style.maxHeight;

    if (accordionMaxHeight == "0px" || accordionMaxHeight.length == 0) {
      accordionContent.style.maxHeight = `${
        accordionContent.scrollHeight + 32
      }px`;
      header.querySelector(".fas").classList.remove("fa-plus");
      header.querySelector(".fas").classList.add("fa-minus");
      header.querySelector(".title").classList.add("font-bold");
    } else {
      accordionContent.style.maxHeight = `0px`;
      header.querySelector(".fas").classList.add("fa-plus");
      header.querySelector(".fas").classList.remove("fa-minus");
      header.querySelector(".title").classList.remove("font-bold");
    }
  });
});

function notificationAction() {
  $("#notification-box").toggle();
  $("#noti-outside").toggle();
}
function messageAction() {
  $("#message-box").toggle();
  $("#mes-outside").toggle();
}
function storeAction() {
  $("#store-box").toggle();
  $("#store-outside").toggle();
}
function profileAction() {
  $(".profile-box").toggle();
  $(".profile-outside").toggle();
}
function toggleSettings() {
  $("#profile-settings").toggle();
}
function dateFilterAction(selector) {
  $(selector).toggle();
  // const checkClassExits = $(selector);
  // if (checkClassExits.hasClass("active")) {
  //   checkClassExits.removeClass("active");
  // } else {
  //   checkClassExits.addClass("active");
  // }
}

// Multi Step Modal in Signin Page
function ModalExist() {
  const modalContent = document.querySelector(".modal-content");

  if (modalContent) {
    // Multi Step Modal in Signin Page
    const modal = document.getElementById("multi-step-modal");
    const stepContents = modalContent.querySelectorAll(".step-content");
    const nextButtons = modalContent.querySelectorAll('[id$="-next"]');
    const cancelButtons = modalContent.querySelectorAll('[id$="-cancel"]');
    const modalOpen = document.querySelector(".modal-open");
    const modalOverlay = document.querySelector(".modal-overlay");

    // Show modal when trigger button is clicked
    modalOpen.addEventListener("click", () => {
      modal.classList.remove("hidden");
    });

    function hideModal() {
      modal.classList.add("hidden");
    }

    // Hide modal when overlay is clicked or close button is clicked
    modalOverlay.addEventListener("click", hideModal);

    let currentStep = 1;

    function showStep(step) {
      stepContents.forEach((stepContent) =>
        stepContent.classList.add("hidden")
      );
      modalContent.querySelector(`.step-${step}`).classList.remove("hidden");
    }

    function setCurrentStep(step) {
      currentStep = step;
      showStep(currentStep);
    }

    function nextStep() {
      setCurrentStep(currentStep + 1);
    }

    cancelButtons.forEach((cancelButton) => {
      cancelButton.addEventListener("click", () => {
        modal.classList.add("hidden");
      });
    });

    nextButtons.forEach((nextButton) => {
      nextButton.addEventListener("click", nextStep);
    });

    setCurrentStep(1);
  }
}

ModalExist();

// Switch Toggle
const switch_btn = document.querySelectorAll(".switch-btn");
if (switch_btn && switch_btn.length > 0) {
  switch_btn.forEach((item, index) => {
    item.addEventListener("click", () => {
      if (switch_btn[index].classList.contains("active")) {
        switch_btn[index].classList.remove("active");
      } else {
        switch_btn[index].classList.add("active");
      }
    });
  });
}

//navigation actions

function navSubmenu() {
  const navSelector = document.querySelector(".nav-wrapper");
  if (navSelector) {
    const navItems = navSelector.querySelectorAll(".item");
    if (navItems && navItems.length > 0) {
      navItems.forEach((item, i) => {
        const submenuExist = navItems[i].querySelector(".sub-menu");
        if (submenuExist) {
          const clickItem = navItems[i].querySelector("a");
          clickItem.addEventListener("click", (e) => {
            e.preventDefault();
            if (submenuExist.classList.contains("active")) {
              submenuExist.classList.remove("active");
            } else {
              submenuExist.classList.add("active");
            }
          });
        } else {
          return false;
        }
      });
    } else {
      return false;
    }
  } else {
    return false;
  }
}
navSubmenu();


// function initModeSetting() {
//   var body = document.body;
//   var lightDarkBtn = document.querySelectorAll('.light-dark-mode');
//   if (lightDarkBtn) {
//     lightDarkBtn.forEach(function (item) {
//       item.addEventListener('click', function (event) {
//         if (body.hasAttribute("data-mode") && body.getAttribute("data-mode") == "dark") {
//           body.setAttribute('data-mode', 'light');
//           sessionStorage.setItem("data-layout-mode", "light");
//         } else {
//           body.setAttribute('data-mode', 'dark');
//           sessionStorage.setItem("data-layout-mode", "dark");
//         }
//       });
//     });
//   }

//   if (sessionStorage.getItem("data-layout-mode") && sessionStorage.getItem("data-layout-mode") == "light") {
//     body.setAttribute('data-mode', 'light');
//   } else if (sessionStorage.getItem("data-layout-mode") == "dark") {
//     body.setAttribute('data-mode', 'dark');
//   }
// }

// initModeSetting()



  // Check the initial theme preference and apply the appropriate class
  if (localStorage.theme === 'dark' || (window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }

  // Toggle the theme when the button is clicked
  var themeToggle = document.getElementById('theme-toggle');
  themeToggle.addEventListener('click', function() {
    // Check the current theme and toggle it
    if (localStorage.theme === 'dark') {
      localStorage.theme = 'light';
    } else {
      localStorage.theme = 'dark';
    }

    // Apply the new theme
    if (localStorage.theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  });

