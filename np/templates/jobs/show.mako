<%inherit file="/base.mako"/>\

<%def name="title()">Job Log</%def>\
<iframe allowtransparency=true frameborder=0 scrolling=auto src="/jobs/${c.jobID}_${c.host}/log" style="width:100%;height:800px"></iframe>
