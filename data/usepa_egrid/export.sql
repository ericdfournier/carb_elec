-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - usepa.egrid_ba_2021
# - usepa.egrid_demo_2021
# - usepa.egrid_gen_2021
# - usepa.egrid_ggl_2021
# - usepa.egrid_nrl_2021
# - usepa.egrid_plnt_2021
# - usepa.egrid_srl_2021
# - usepa.egrid_st_2021
# - usepa.egrid_unt_2021
# - usepa.egrid_us_2021
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy usepa.egrid_ba_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_ba_2021.csv' (format csv, header true);
\copy usepa.egrid_demo_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_demo_2021.csv' (format csv, header true);
\copy usepa.egrid_gen_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_gen_2021.csv' (format csv, header true);
\copy usepa.egrid_ggl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_ggl_2021.csv' (format csv, header true);
\copy usepa.egrid_nrl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_nrl_2021.csv' (format csv, header true);
\copy usepa.egrid_plnt_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_plnt_2021.csv' (format csv, header true);
\copy usepa.egrid_srl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_srl_2021.csv' (format csv, header true);
\copy usepa.egrid_st_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_st_2021.csv' (format csv, header true);
\copy usepa.egrid_unt_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_unt_2021.csv' (format csv, header true);
\copy usepa.egrid_us_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_egrid_us_2021.csv' (format csv, header true);
