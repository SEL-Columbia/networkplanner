<%def name='formatSelect(selectID, selectValue, optionPacks)'>
<select id=${selectID} class=lockOnSave>
% for value, name in optionPacks:
<option value=${value}\
% if value == selectValue:
 selected\
% endif
>${name}</option>
% endfor
</select>
</%def>
