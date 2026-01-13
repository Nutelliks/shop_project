// Toggle password visibility for inputs that have a paired .toggle-password button
$(document).ready(function() {
    $(document).on('click', '.toggle-password', function(e) {
        e.preventDefault();
        var targetSelector = $(this).data('target');
        var $input = $(targetSelector);
        if (!$input.length) {
            return;
        }
        // Toggle type
        var wasPassword = $input.attr('type') === 'password';
        $input.attr('type', wasPassword ? 'text' : 'password');
        // Now update icons: show eye when hidden (type=password), eye-slash when visible (type=text)
        var nowIsPassword = $input.attr('type') === 'password';
        $(this).find('.icon-show').toggleClass('d-none', !nowIsPassword);
        $(this).find('.icon-hide').toggleClass('d-none', nowIsPassword);
        $(this).attr('aria-pressed', nowIsPassword ? 'false' : 'true');
    });
});