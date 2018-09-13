var utils = require("common/util");

utils.inject_css("pl_tbi", ".pl_tbi { display: none; } ");

var _injected = {};
function ScopedCss(name) {
  if (!_injected[name]) {
    $C(name, function(m) {
      if (_injected[name]) {
        return;
      }

      utils.inject_css("scoped_"+name, m.css);
      _injected[name] = true;
    });
  }

  return "pl_tbi scoped_" + name;
}

module.exports = ScopedCss;
