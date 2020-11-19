import os
installscript = """'display alert "Install the `nought` command on this computer?" buttons {"No", "Yes"}
if button returned of result = "No" then
     display alert "OK, nothing was installed!"
else
    if button returned of result = "Yes" then
         display alert "Yes was clicked"
    end if
end if'
"""
os.system("osascript -e "+installscript)