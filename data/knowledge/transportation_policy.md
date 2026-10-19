
# Transportation Optimization Policy

## Objective
The primary objective is to minimize total transportation cost while satisfying store demand and respecting distribution center capacity.

## Capacity constraints
The total quantity shipped from a distribution center cannot exceed its available capacity.

## Demand fulfillment
Each store's demand should be satisfied whenever sufficient feasible transportation capacity exists.

## Insufficient capacity
If available capacity is insufficient to satisfy demand, the optimization system must report the shortfall. It must not silently discard demand.

## External fulfillment
External fulfillment providers may be considered only when explicitly enabled in the optimization configuration.

## Infeasible optimization
When no feasible solution exists, the solver must return an infeasible status and explain which constraints prevent feasibility.
