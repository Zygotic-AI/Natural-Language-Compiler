# Emit pipeline gates

Code is emitted only when the action is on the plan and the decisions for that action are bound. A missing decision stops the compiler. The gate stays closed until the plan and the decisions line up, which is how NLC keeps changes that never entered the graph out of the codebase an audit will later read.
