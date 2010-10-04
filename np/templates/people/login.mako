<%inherit file="/base.mako"/>

<%def name="title()">Login</%def>

<%def name="head()">
${h.javascript_link('/files/recaptcha_ajax.js')}
</%def>

<%def name="css()">
#reset {display: none}
#resetForm {display: none}
</%def>

<%def name="js()">
// Prepare login form
var rejection_count = 0;
function ajax_login() {
    // Validate
    var errorCount = 0;
    errorCount = errorCount + isEmpty('username');
    errorCount = errorCount + isEmpty('password');
    if (errorCount) {
        $('#reset').hide();
        return;
    }
    // Initialize
    var loginData = {
        'username': $('#username').val(),
        'password': $('#password').val(),
        'minutesOffset': $('#minutesOffset').val()
    }
    // Get recaptcha
    if ($('#recaptcha_challenge_field').length) {
        loginData['recaptcha_challenge_field'] = $('#recaptcha_challenge_field').val();
        loginData['recaptcha_response_field'] = $('#recaptcha_response_field').val();
    }
    // Attempt login
    $.post("${h.url('person_login_')}", loginData, function(data) {
        if (data.isOk) {
            window.location = "${c.targetURL}";
        } else {
            // Give feedback
            $('#reset').show();
            $('#resetLink').show();
            $('#resetForm').hide();
            // Update rejection count
            rejection_count = data.rejection_count ? data.rejection_count : rejection_count + 1;
            // If there have been too many rejections,
            if (rejection_count >= ${h.REJECTION_LIMIT}) {
                Recaptcha.create("${c.publicKey}", 'recaptcha', {
                    theme: 'red',
                    callback: Recaptcha.focus_response_field
                });
            }
        }
    }, 'json');
}
$('#login_button').click(ajax_login);
function isEmpty(inputID) {
    var input = $('#' + inputID);
    var output = $('#m_' + inputID);
    if (input.val() == '') {
        output.text('You must provide a ' + inputID);
        input.focus();
        return 1;
    } else {
        output.text('');
        return 0;
    }
}
$('#password').keydown(function(e) {
    if (e.keyCode == 13) ajax_login();
});

// Prepare reset form
$('#resetLink').click(function() {
    $('#resetLink').hide();
    $('#resetForm').show();
    $('#resetEmail').val('').keydown(function(e) {
        if (e.keyCode == 13) ajax_reset();
    }).focus();
});
$('#resetButton').click(ajax_reset);
function ajax_reset() {
    // Check that the email is not empty
    var email = $.trim($('#resetEmail').val());
    if (!email) {
        $('#resetEmail').focus();
        return;
    }
    // Post
    $('.lockOnReset').attr('disabled', true);
    $.post("${h.url('person_reset')}", {
        'email': email
    }, function(data) {
        if (data.isOk) {
            $('#m_password').html('Please check your email');
        } else {
            $('#m_password').html('Email not found');
            $('.lockOnReset').removeAttr('disabled');
        }
    }, 'json');
}

// Configure
$('#username').focus();
$('#minutesOffset').val(new Date().getTimezoneOffset());
</%def>

<%def name="toolbar()">
<a class=linkOFF href="${h.url('person_register')}" id=register>Register for an account</a>
</%def>

<table>
<tr>
<td><label for=username>Username</label></td>
<td><input id=username></td>
<td>
<span id=m_username>
${dict(updated='Account updated', created='Account created', expired='Ticket expired').get(c.messageCode, '')}
</span>
<span id=reset>
<a id=resetLink class=linkOFF>Did you forget your login?</a>
<span id=resetForm>
Email
<input class=lockOnReset id=resetEmail>
<input class=lockOnReset id=resetButton type=button value=Reset>
</span>
</span>
</td>
</tr>
<tr>
<td><label for=password>Password</label></td>
<td><input id=password type=password></td>
<td id=m_password></td>
</tr>
<tr>
<td><label for=minutesOffset>Time</label</td>
<td>
<select id=minutesOffset>
<%include file='/people/offsets.mako'/>\
</select>
</td>
<td id=m_minutesOffset></td>
</tr>
</table>
<div id=recaptcha></div>
<input id=login_button type=button value=Login><br>
<br>
<a class=linkOFF href="/docs">Read documentation for ${h.SITE_NAME} v${h.SITE_VERSION}</a>
