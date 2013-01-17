<%inherit file="/base.mako"/>\

<%def name="title()">Job Index</%def>\

<%def name="css()">
td {padding-right: 1em}
</%def>

<%def name="js()">

$('.kill').click(function() {
    var job_pid_host = /([^_]+)_(.*)/.exec(this.id);
    var job_pid = job_pid_host[1];
    var host = job_pid_host[2];
    if (confirm('Are you sure you want to kill job PID ' + job_pid + ', on host: ' + host + '?')) {
        $.ajax({
            type:  'GET', 
            url: '/jobs/' + job_pid + '_' + host + '/kill', 
            success: function(data) {
                if (data.isOk) {
                    setTimeout(function() {window.location = "/jobs";}, 1000);
                } else {
                    alert("Failed to kill job");
                }
            },
            dataType: 'json'});
    }
});

</%def>

<table>
    <tr>
        <td><b>PID</b></td>
        <td><b>Host</b></td>
        <td><b>Start Time</b></td>
        <td><b>End Time</b></td>
        <td></td>
    </tr>
% for job in c.jobs:
    <tr>
        <td>${job.pid}</td>
        <td>${job.host}</td>
        <td>${job.start_time}</td>
        <td>${job.end_time}
        % if (not job.end_time) and (h.isAdmin()):
            <a class='linkOFF kill' id="${job.pid}_${job.host}">Kill</a>
        % endif
        </td>
        <td>
        <a class=linkOFF href="/jobs/${job.pid}_${job.host}">View</a>
        </td>
    </tr>
% endfor
</table>
