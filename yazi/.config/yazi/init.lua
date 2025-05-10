
require("full-border"):setup {
	-- Available values: ui.Border.PLAIN, ui.Border.ROUNDED
	type = ui.Border.ROUNDED,
}

require("smart-enter"):setup {
	open_multi = true,
}

-- require("simple-mtpfs"):setup({})

-- -- In yazi.toml change linemode = "permissions_and_size"
-- function Linemode:permissions_and_size()
-- 	local size = self._file:size()
-- 	local perms = self._file.cha:perm()
-- 	return string.format("%s %s", perms, size and ya.readable_size(size) or "-")
-- end
