#!/usr/bin/env perl

use warnings;
use strict;
use 5.10.1;

use File::Slurp;

my $base_fn = 'run.m';
my $template_ext = '.template';

my $param_fn_base = 'params_';
my $param_ext = '.txt';

my %params = (
    __NITROGEN_RATIO__ => 0.30,
    __CARBON_RATIO__ => 1.0,
    __FIXED_OXYGEN_LEVEL__ => 75.0,
    __FIXED_OXYGEN_DIFFUSION__ => 1e4,
    __FIXED_CO2_LEVEL__ => 600,
    __T_MAX__ => 25.0,
    __FE_PRECIPITATION__ => 0.1,
);

my $out_fn_mask = '__OUT__';
my $out_fn_base = 'rates_';
my $out_fn_ext = '.csv';

my @multipliers = (0.99, 1.00, 1.01);

# read in the template file
my $base_file = read_file($base_fn . $template_ext);

my $i = 0;

# modulate each of the parameters in turn
while (my ($this_param, $base_value) = each %params) {
    say "manipulating $this_param";
    # when modulating this parameter, multiply by some multiplier
    for my $multiplier (@multipliers) {
        $params{$this_param} = $base_value * $multiplier;

        # go through each pair of params and values, replacing the param placeholder
        # with the value for this loop
        my $file = $base_file;
        while (my ($p, $v) = each %params) {
            $file =~ s/$p/$v/g;
        }

        # write this new script to a file
        my $out_fn = $out_fn_base . $i . $out_fn_ext;
        #write_file($out_fn, $file);

        # write the parameters to a separate file
        my $param_fn = $param_fn_base . $i . $param_ext;
        my $param_file = join "\n", join "\t", each %params;
        #write_file($param_fn, $param_file);

        $i++;
        my $x = <STDIN>;
    }

    # reset the parameter to its base value
    $params{$this_param} = $base_value;
}



__END__
