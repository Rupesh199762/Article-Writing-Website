$(document).ready(function() {
    $('#party_list').change(function() {
        var selectedValue = $(this).val();
        $.ajax({
            url: '/get_company_list/',
            data: {
                'selected_value': selectedValue
            },
            dataType: 'json',
            success: function(data) {
                $('#company_list').empty();
                $('#company_list').append('<option value=""> Select indivisual/Company Name </option>');
                $('#company_list').append('<option value="All">ALL</option>');
                $.each(data, function(index, options) {
                    $('#company_list').append('<option value="' + options + '">' + options + '</option>');
                });
            }
        });
    });
});