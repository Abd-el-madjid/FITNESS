const searchButton = document.querySelector("#search_button");
const searchInput = document.querySelector("#search-orders");

searchButton.addEventListener("click", () => {
  const searchValue = searchInput.value.trim().toLowerCase();
  const rows = document.querySelectorAll(".row101");

  rows.forEach((row) => {
    const cells = row.querySelectorAll(".cell100");
    let isMatch = false;

    cells.forEach((cell) => {
      if (cell.textContent.trim().toLowerCase().includes(searchValue)) {
        isMatch = true;
      }
    });

    if (isMatch) {
      row.style.display = "table-row";
    } else {
      let rowText = row.textContent.trim().toLowerCase();
      if (rowText.includes(searchValue)) {
        row.style.display = "table-row";
      } else {
        row.style.display = "none";
      }
    }
  });
});

function modifier_button_empl() {
  $("#modifie_rdv_form").toggleClass("none");
  console.log("i m here");

  console.log(" date_search_bar_container info open ");
}

function delet_button_empl(id) {
  $("#delet_rdv_form").toggleClass("none");
  $("input[name=club_id]").val(id);

  console.log("i work");
  console.log(" date_search_bar_container info open ");
}
function submit(event) {
  event.preventDefault(); // prevent the default behavior of the cancel button
  event.target.form.submit(); // submit the form element
}
function modifierEmployee(id) {
  event.preventDefault();
   // retrieve club id from somewhere, like an attribute of the clicked element
    // AJAX request to fetch club information
  $.ajax({
      
      url: `/nutrition/clubs/request_info/${id}`,
      type: "GET",
      dataType: "json",
      success: function (response) {
        // Populate the form fields with the received club information
       $("#logo_src").attr("src", response.logo_url);

        $('#modifie_rdv_form input[name="club_id"]').val(response.id);
        $('#modifie_rdv_form input[name="club_name"]').val(response.club_name);
        $('#modifie_rdv_form select[name="club_type"]').val(response.club_type);
        $('#modifie_rdv_form input[name="club_date_of_creation"]').val(
          response.date_of_creation
        );

        // Show the form
        $("#modifie_rdv_form").removeClass("none");
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
        alert("Failed to fetch club information.");
      },
    });
}



function selected_change_filter() {
  // Get the selected option
  const selectElement = document.getElementById("select-filter");
  const selectedOption = selectElement.value.toLowerCase();

  // Get a reference to all the rows in the table
  const rows = document.querySelectorAll(".table100 .row101");

  // Iterate through all the rows and hide/show them based on the selected option
  rows.forEach((row) => {
    const typeCell = row.querySelector('.cell100[data-title="Club Type"]');
    const actionValue = typeCell.innerText.toLowerCase().trim();

    if (selectedOption === "All Types") {
      row.style.display = "table-row";
    } else if (actionValue === selectedOption) {
      row.style.display = "table-row";
    } else {
      row.style.display = "none";
    }
  });
}


