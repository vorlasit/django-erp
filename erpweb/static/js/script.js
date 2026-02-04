
/**
 * Confirm delete with SweetAlert
 * @param {Event} event - click event
 * @param {string} url - delete URL
 */

document.addEventListener('DOMContentLoaded', function () {

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  document.querySelectorAll('.btn-delete').forEach(function (button) {
    button.addEventListener('click', function (event) {
      event.preventDefault() // ❌ หยุดการลบทันที
      const url = this.getAttribute('href')
      const username = this.dataset.name || 'this user'

      Swal.fire({
        title: `Delete ${username}?`,
        text: 'This action cannot be undone!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel'
      }).then((result) => {
        if (result.isConfirmed) {
          // ✅ ไปยัง URL ลบ
          window.location.href = url
        }
      })
    })
  }) 
})

