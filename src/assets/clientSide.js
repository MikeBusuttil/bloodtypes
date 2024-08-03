const bloodTypes = new Set(['A-', "A+", 'B-', "B+", 'AB-', "AB+", 'O-', "O+", "all"]);

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
      large_params_function: function(hoverData, previously_selected_type) {
        node_type = hoverData?.['points']?.[0]?.['customdata'] || 'all'
        if (!bloodTypes.has(node_type) || node_type === previously_selected_type) {
          return window.dash_clientside.no_update;
        }
        return node_type;
      }
  }
});
