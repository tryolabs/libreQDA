function simpleModal(buttonId, modalId) {
    $(document).ready(function() {
        $('#buttonId').click(function(ev) {
            ev.preventDefault(); // prevent navigation
            var url = $(this).data("url"); // get the form url
            $.getJSON(url, function(data) { // load the url into the modal
                $('#modalId').html(data.html);
                $("#modalId").modal('show');
            });
            return false; // prevent the click propagation
        });
        $('#modalId').on('submit', 'form', function() {
            $.ajax({
                type : $(this).attr('method'),
                url : this.action,
                data : $(this).serialize(),
                context : this,
                success : function(data, status) {
                    if (data.redirect) {
                        window.location.replace(data.redirect);
                    }
                    $('#modalId').html(data.html);
                }
            });
            return false;
        });
    });
}
