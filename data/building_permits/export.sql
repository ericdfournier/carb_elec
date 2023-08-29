-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - permits.class_definitions
 * - permits.combined
 * - permits.panel_upgrades
 * - permits.panel_upgrades_geocode_arcgis
 * - permits.panel_upgrades_geocoded
 * - permits.panel_upgrades_geocoded_geographies
 * - permits.sampled_counties
 * - permits.sampled_places
 * - permits.sampled_territories
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy permits.class_definitions to '/Users/edf/repos/carb_elec/dump/csv/permits_class_definitions.csv' (format csv, header true);
\copy permits.combined to '/Users/edf/repos/carb_elec/dump/csv/permits_combined.csv' (format csv, header true);
\copy permits.panel_upgrades to '/Users/edf/repos/carb_elec/dump/csv/permits_panel_upgrades.csv' (format csv, header true);
\copy permits.panel_upgrades_geocode_arcgis to '/Users/edf/repos/carb_elec/dump/csv/permits_panel_upgrades_geocode_arcgis.csv' (format csv, header true);
\copy permits.panel_upgrades_geocoded to '/Users/edf/repos/carb_elec/dump/csv/permits_panel_upgrades_geocoded.csv' (format csv, header true);
\copy permits.panel_upgrades_geocoded_geographies to '/Users/edf/repos/carb_elec/dump/csv/permits_panel_upgrades_geocoded_geographies.csv' (format csv, header true);
\copy permits.sampled_counties to '/Users/edf/repos/carb_elec/dump/csv/permits_sampled_counties.csv' (format csv, header true);
\copy permits.sampled_places to '/Users/edf/repos/carb_elec/dump/csv/permits_sampled_places.csv' (format csv, header true);
\copy permits.sampled_territories to '/Users/edf/repos/carb_elec/dump/csv/permits_sampled_territories.csv' (format csv, header true);
