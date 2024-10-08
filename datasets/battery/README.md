## Band gap
The band gap is calculated by the energy difference between the lowest unoccupied band and the highest occupied band in all k-points.

## Voltage
Here, the voltage of a battery system is calculated as the energy to loss one Li or Na:
```
V = -1 * [E(C_(1-X)MO_2) - E(C_(1-Y)MO_2) - (Y-X)E(C)] / (Y - X)    (Y>X)
```
Where C is Li or Na, and M is the metal, X/Y is the loss ratio of Li or Na.

## Reference
### QE
The calculation of QE using the same pseudopotential, energy cutoff, k-point mesh, smearing method, and U value. The version of QE is 7.0.

### VASP
For VASP, using PAW pseudopotential, the ENCUT is 520 eV, KSPACING is 0.25 1/Angstrom, smearing is Gaussian with a width of 0.05 eV, and the U is same as ABACUS. The version of VASP is 5.4.4. All the structures are optimized first, and then a single point calculation is performed.