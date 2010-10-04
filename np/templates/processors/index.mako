<%inherit file="/base.mako"/>\

<%def name="title()">Processor Index</%def>\

<%def name="toolbar()">
${len(c.processors)} processor${'s' if len(c.processors) != 1 else ''} online
</%def>

<%def name="css()">
td {padding-right: 1em}
</%def>

<table>
    <tr>
        <td><b>ID</b></td>
        <td><b>Updated</b></td>
    </tr>
% for processor in c.processors:
    <tr>
        <td>${processor.id}</td>
        <td>${h.getWhenIO().format(processor.when_updated)}</td>
    </tr>
% endfor
</table>
