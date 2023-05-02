-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - usepa.ba_2021
# - usepa.demo_2021
# - usepa.gen_2021
# - usepa.ggl_2021
# - usepa.nrl_2021
# - usepa.plnt_2021
# - usepa.srl_2021
# - usepa.st_2021
# - usepa.unt_2021
# - usepa.us_2021
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy usepa.ba_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_ba_2021.csv' (format csv, header true);
\copy usepa.demo_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_demo_2021.csv' (format csv, header true);
\copy usepa.gen_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_gen_2021.csv' (format csv, header true);
\copy usepa.ggl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_ggl_2021.csv' (format csv, header true);
\copy usepa.nrl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_nrl_2021.csv' (format csv, header true);
\copy usepa.plnt_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_plnt_2021.csv' (format csv, header true);
\copy usepa.srl_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_srl_2021.csv' (format csv, header true);
\copy usepa.st_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_st_2021.csv' (format csv, header true);
\copy usepa.unt_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_unt_2021.csv' (format csv, header true);
\copy usepa.us_2021 to '/Users/edf/repos/carb_elec/dump/csv/usepa_us_2021.csv' (format csv, header true);
