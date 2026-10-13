"""
Edexcel GCSE maths topics
Numbers
Algebra
Ratio, Proportion & Rates of change
Geometry and measures
Statistics & Probability

Each subtopic has a name and a description written for a labelling AI:
what the question asks the student to do, and how to tell it apart
from similar subtopics.
"""

TOPICS = {
    "Number basics": [
        {
            "name": "Ordering numbers",
            "description": "Putting integers, decimals or negative numbers in ascending or descending order, or comparing two numbers.",
        },
        {
            "name": "Four operations with integers",
            "description": "Adding, subtracting, multiplying or dividing whole numbers, including written methods such as long multiplication and short or long division.",
        },
        {
            "name": "Four operations with decimals",
            "description": "Adding, subtracting, multiplying or dividing decimals, including money calculations without a calculator.",
        },
        {
            "name": "Negative numbers",
            "description": "Calculating with negative numbers, such as temperature changes, or adding, subtracting, multiplying and dividing with negatives.",
        },
        {
            "name": "Place value",
            "description": "The value of a digit in a number, multiplying or dividing by powers of 10, or using a given fact (e.g. 23 x 47 = 1081) to work out related calculations.",
        },
        {
            "name": "Order of operations",
            "description": "Using BIDMAS/BODMAS to evaluate an expression, or inserting brackets to make a calculation correct.",
        },
        {
            "name": "Inverse operations",
            "description": "Undoing an operation to find a starting value, e.g. number machines worked backwards, or checking a result with the inverse operation.",
        },
        {
            "name": "Inequality symbols",
            "description": "Using <, >, <=, >=, = or != to compare numbers or quantities. Not for solving inequalities with unknowns.",
        },
        {
            "name": "Systematic listing",
            "description": "Listing all possible combinations or outcomes in an organised way, e.g. all the meal choices from a menu.",
        },
        {
            "name": "Product rule for counting",  # N5, Higher
            "description": "Counting arrangements by multiplying the number of choices at each stage, e.g. how many 4-digit codes are possible. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A number basics question that fits none of the subtopics above.",
        },
    ],
    "Factors, multiples and primes": [
        {
            "name": "Prime numbers",
            "description": "Identifying or listing prime numbers, or reasoning about whether a number is prime.",
        },
        {
            "name": "Factors and multiples",
            "description": "Listing factors or multiples of a number, or identifying them from a list. Not for HCF/LCM.",
        },
        {
            "name": "HCF and LCM",
            "description": "Finding the highest common factor or lowest common multiple, including word problems such as when two buses next arrive together.",
        },
        {
            "name": "Prime factorisation",
            "description": "Writing a number as a product of its prime factors, often with a factor tree or in index form, e.g. 360 = 2^3 x 3^2 x 5.",
        },
        {
            "name": "Other",
            "description": "A factors, multiples or primes question that fits none of the subtopics above.",
        },
    ],
    "Powers, roots and standard form": [
        {
            "name": "Powers and roots",
            "description": "Squares, cubes, square roots and cube roots of numbers, and recognising square and cube numbers.",
        },
        {
            "name": "Estimating powers and roots",  # N6, Higher
            "description": "Estimating the value of a power or root that is not exact, e.g. which two integers the square root of 50 lies between. Higher tier.",
        },
        {
            "name": "Calculating with roots and integer indices",
            "description": "Evaluating numerical expressions with positive, zero or negative integer powers and roots, e.g. 2^-3 or 5^0.",
        },
        {
            "name": "Fractional indices",  # N7, Higher
            "description": "Evaluating or simplifying numbers raised to fractional powers, e.g. 27^(2/3) or 16^(-1/2). Higher tier.",
        },
        {
            "name": "Surds",  # N8, Higher
            "description": "Simplifying surds, e.g. sqrt(48) = 4sqrt(3), and adding, multiplying or expanding brackets with surds. Higher tier.",
        },
        {
            "name": "Rationalising denominators",  # N8, Higher
            "description": "Removing a surd from the denominator of a fraction, e.g. 6/sqrt(3) or 1/(2 + sqrt(5)). Higher tier.",
        },
        {
            "name": "Standard form",
            "description": "Writing numbers in or out of standard form (a x 10^n) and calculating with numbers in standard form.",
        },
        {
            "name": "Other",
            "description": "A powers, roots or standard form question that fits none of the subtopics above.",
        },
    ],
    "Fractions": [
        {
            "name": "Adding and subtracting fractions",
            "description": "Adding or subtracting fractions or mixed numbers, usually by finding a common denominator.",
        },
        {
            "name": "Multiplying and dividing fractions",
            "description": "Multiplying or dividing fractions or mixed numbers.",
        },
        {
            "name": "Mixed numbers and improper fractions",
            "description": "Converting between mixed numbers and improper fractions, or simplifying and finding equivalent fractions.",
        },
        {
            "name": "Converting between fractions and decimals",
            "description": "Writing a fraction as a decimal or a terminating decimal as a fraction, including ordering a mix of fractions and decimals.",
        },
        {
            "name": "Recurring decimals to fractions",  # N10, Higher
            "description": "Proving or showing algebraically that a recurring decimal equals a fraction, e.g. 0.4545... = 5/11. Higher tier.",
        },
        {
            "name": "Fractions of an amount",
            "description": "Finding a fraction of a quantity, e.g. 3/5 of 40, or word problems where a fraction of something is used or left over.",
        },
        {
            "name": "Exact answers with fractions and pi",
            "description": "Giving answers exactly as fractions or in terms of pi rather than as rounded decimals, e.g. 'give your answer in terms of pi'.",
        },
        {
            "name": "Other",
            "description": "A fractions question that fits none of the subtopics above.",
        },
    ],
    "Estimation and accuracy": [
        {
            "name": "Estimating and checking answers",
            "description": "Estimating a calculation by rounding each number to 1 significant figure, or judging whether an answer is an over- or underestimate.",
        },
        {
            "name": "Rounding (decimal places, significant figures)",
            "description": "Rounding numbers to a given number of decimal places, significant figures, or to the nearest 10, 100 etc.",
        },
        {
            "name": "Error intervals",
            "description": "Writing the error interval for a rounded or truncated number using inequalities, e.g. 6.5 <= x < 7.5.",
        },
        {
            "name": "Limits of accuracy",
            "description": "Finding the smallest and largest values a rounded measurement could have been. Not for calculations combining bounds.",
        },
        {
            "name": "Upper and lower bounds",  # N16, Higher
            "description": "Using upper and lower bounds in a calculation, e.g. the maximum possible area or speed from rounded measurements. Higher tier.",
        },
        {
            "name": "Other",
            "description": "An estimation or accuracy question that fits none of the subtopics above.",
        },
    ],
    "Units and measures": [
        {
            "name": "Standard units and conversions",
            "description": "Converting between metric units of length, mass, capacity, area or volume, or between units of time, money and currency.",
        },
        {
            "name": "Other",
            "description": "A units and measures question that fits none of the subtopics above.",
        },
    ],
    "Algebraic expressions": [
        {
            "name": "Algebraic notation and vocabulary",
            "description": "Writing expressions using algebraic notation, or identifying whether something is an expression, equation, formula, identity or term.",
        },
        {
            "name": "Simplifying expressions",
            "description": "Collecting like terms, or simplifying products and quotients of terms such as 3a x 4b.",
        },
        {
            "name": "Expanding brackets",
            "description": "Multiplying out single, double or triple brackets, e.g. 3(x + 2) or (x + 3)(x - 5).",
        },
        {
            "name": "Factorising",
            "description": "Taking out a common factor to put an expression into a single bracket, e.g. 6x + 9 = 3(2x + 3). Not for quadratics.",
        },
        {
            "name": "Factorising quadratics",
            "description": "Factorising x^2 + bx + c into two brackets, including the difference of two squares.",
        },
        {
            "name": "Factorising non-monic quadratics",  # Higher only
            "description": "Factorising quadratics where the x^2 coefficient is not 1, e.g. 2x^2 + 7x + 3. Higher tier.",
        },
        {
            "name": "Laws of indices",
            "description": "Simplifying algebraic expressions with powers using the index laws, e.g. x^3 x x^5 or (2a^2)^3.",
        },
        {
            "name": "Algebraic fractions",  # Higher only
            "description": "Simplifying, adding, subtracting, multiplying or dividing fractions that contain algebra, often after factorising. Higher tier.",
        },
        {
            "name": "Identities and equivalent expressions",
            "description": "Showing two expressions are equivalent, using the identity symbol, or finding unknown constants so an identity holds.",
        },
        {
            "name": "Algebraic proof",  # Higher only
            "description": "Proving a general statement with algebra, e.g. that the sum of three consecutive integers is a multiple of 3, using 2n, 2n + 1 etc. Higher tier.",
        },
        {
            "name": "Other",
            "description": "An algebraic expressions question that fits none of the subtopics above.",
        },
    ],
    "Formulae and functions": [
        {
            "name": "Substituting into formulae",
            "description": "Working out the value of an expression or formula by substituting given values, e.g. v = u + at.",
        },
        {
            "name": "Rearranging formulae",
            "description": "Changing the subject of a formula, including when the subject appears twice or under a power or root.",
        },
        {
            "name": "Functions",
            "description": "Using function notation f(x) to evaluate a function, or number machines that represent a function.",
        },
        {
            "name": "Inverse and composite functions",  # Higher only
            "description": "Finding f^-1(x) or composite functions such as fg(x). Higher tier.",
        },
        {
            "name": "Other",
            "description": "A formulae or functions question that fits none of the subtopics above.",
        },
    ],
    "Graphs": [
        {
            "name": "Coordinates in four quadrants",
            "description": "Plotting or reading coordinates, including the midpoint of a line segment.",
        },
        {
            "name": "Plotting straight-line graphs",
            "description": "Completing a table of values and drawing a straight-line graph, or plotting horizontal and vertical lines.",
        },
        {
            "name": "Gradient and intercepts",
            "description": "Finding the gradient or y-intercept of a straight line from a graph, two points or an equation.",
        },
        {
            "name": "Equation of a straight line",
            "description": "Finding the equation y = mx + c of a line from its gradient and a point, or from two points.",
        },
        {
            "name": "Parallel and perpendicular lines",
            "description": "Using gradients to identify or find parallel lines, or perpendicular lines (Higher), and their equations.",
        },
        {
            "name": "Quadratic graphs",
            "description": "Plotting a quadratic graph from a table of values, or finding its roots, intercepts and turning point.",
        },
        {
            "name": "Recognising and sketching graphs",
            "description": "Matching equations to graph shapes (linear, quadratic, cubic, reciprocal), or sketching them.",
        },
        {
            "name": "Exponential graphs",  # Higher only
            "description": "Graphs of the form y = k^x, including growth and decay contexts. Higher tier.",
        },
        {
            "name": "Trigonometric graphs",  # Higher only
            "description": "The graphs of y = sin x, cos x and tan x, and reading or solving values from them. Higher tier.",
        },
        {
            "name": "Graph transformations",  # Higher only
            "description": "Translating or reflecting a graph, e.g. y = f(x + a) or y = -f(x), and describing the transformation. Higher tier.",
        },
        {
            "name": "Real-life graphs",
            "description": "Interpreting or drawing graphs in context, e.g. distance-time, velocity-time, conversion or cost graphs.",
        },
        {
            "name": "Gradients and areas under curves",  # Higher only
            "description": "Estimating the gradient of a curve with a tangent, or the area under a graph, and interpreting them, e.g. acceleration or distance. Higher tier.",
        },
        {
            "name": "Equation of a circle",  # Higher only
            "description": "Using x^2 + y^2 = r^2 for a circle centred at the origin, or finding the tangent to a circle at a point. Higher tier.",
        },
        {
            "name": "Geometry problems on coordinate axes",
            "description": "Shapes drawn on coordinate axes, e.g. finding a missing vertex of a square or the area of a shape from its coordinates.",
        },
        {
            "name": "Other",
            "description": "A graphs question that fits none of the subtopics above.",
        },
    ],
    "Equations and inequalities": [
        {
            "name": "Linear equations",
            "description": "Solving linear equations, including those with brackets, fractions or unknowns on both sides.",
        },
        {
            "name": "Forming equations and formulae",
            "description": "Writing an equation or formula from a word problem or diagram, then usually solving it.",
        },
        {
            "name": "Solve quadratic equations by factorising",
            "description": "Solving a quadratic equation equal to zero by factorising it.",
        },
        {
            "name": "Completing the square",  # Higher only
            "description": "Writing a quadratic in the form (x + p)^2 + q, solving with it, or finding a turning point from it. Higher tier.",
        },
        {
            "name": "Quadratic formula",  # Higher only
            "description": "Solving a quadratic equation with the quadratic formula, often giving answers to a set accuracy. Higher tier.",
        },
        {
            "name": "Simultaneous equations",
            "description": "Solving two linear equations together by elimination or substitution, including forming them from a context.",
        },
        {
            "name": "Simultaneous equations with a quadratic",  # Higher only
            "description": "Solving a linear and a quadratic equation together, e.g. a line meeting a circle or curve. Higher tier.",
        },
        {
            "name": "Solving equations using graphs",
            "description": "Finding approximate solutions by reading where graphs cross each other or the x-axis.",
        },
        {
            "name": "Iteration",  # Higher only
            "description": "Using an iterative formula x_(n+1) = ... to find approximate solutions, or showing a root lies between two values. Higher tier.",
        },
        {
            "name": "Linear inequalities",
            "description": "Solving linear inequalities, showing solutions on a number line, or listing integer values that satisfy them.",
        },
        {
            "name": "Quadratic inequalities",  # Higher only
            "description": "Solving inequalities containing x^2, e.g. x^2 - 5x + 6 < 0. Higher tier.",
        },
        {
            "name": "Inequalities on graphs",  # Higher only
            "description": "Shading or identifying a region on a graph that satisfies several inequalities. Higher tier.",
        },
        {
            "name": "Other",
            "description": "An equations or inequalities question that fits none of the subtopics above.",
        },
    ],
    "Sequences": [
        {
            "name": "Generating terms of a sequence",
            "description": "Continuing a sequence, using a term-to-term rule or a position-to-term rule to find terms, or pattern sequences of shapes.",
        },
        {
            "name": "Fibonacci-type sequences",
            "description": "Sequences where each term is the sum of the previous two, including finding missing terms algebraically.",
        },
        {
            "name": "Nth term of linear sequences",
            "description": "Finding or using the nth term of an arithmetic sequence, e.g. 4n - 1, or deciding if a number is in the sequence.",
        },
        {
            "name": "Quadratic sequences",
            "description": "Sequences with a constant second difference, including finding the nth term an^2 + bn + c (Higher).",
        },
        {
            "name": "Geometric sequences",
            "description": "Sequences with a common ratio, e.g. 3, 6, 12, 24, including surd or algebraic terms (Higher).",
        },
        {
            "name": "Other",
            "description": "A sequences question that fits none of the subtopics above.",
        },
    ],
    "Ratio": [
        {
            "name": "Simplifying ratios",
            "description": "Writing a ratio in its simplest form or in the form 1:n, including ratios with different units.",
        },
        {
            "name": "Sharing in a ratio",
            "description": "Dividing an amount in a given ratio, or finding the total when one share or the difference between shares is known.",
        },
        # "Quantities as fractions and ratios", not needed if labelled right
        {
            "name": "Ratio problems in context",
            "description": "Multi-step ratio word problems, e.g. recipes, mixing paint, or combining two ratios.",
        },
        {
            "name": "Scale drawings and maps",
            "description": "Using a scale or map ratio, e.g. 1:25000, to convert between drawing and real distances.",
        },
        {
            "name": "Other",
            "description": "A ratio question that fits none of the subtopics above.",
        },
    ],
    "Percentages": [
        {
            "name": "Percentage of an amount",
            "description": "Finding a percentage of a quantity, with or without a calculator.",
        },
        # "Converting fractions, decimals and percentages",
        {
            "name": "One quantity as a percentage of another",
            "description": "Writing one amount as a percentage of another, including percentage change and percentage profit or loss.",
        },
        {
            "name": "Percentage increase and decrease",
            "description": "Increasing or decreasing an amount by a percentage, e.g. sale prices or VAT, often with multipliers.",
        },
        {
            "name": "Reverse percentages",
            "description": "Finding the original amount before a percentage change, e.g. the price before a 20% discount.",
        },
        {
            "name": "Simple interest",
            "description": "Interest that is calculated on the original amount only, the same each year.",
        },
        {
            "name": "Compound interest",
            "description": "Interest added each year and then earning interest itself, using a multiplier to a power, e.g. 1.03^5.",
        },
        {
            "name": "Growth and decay",
            "description": "Repeated percentage change outside of interest, e.g. depreciation or population growth, using multipliers.",
        },
        {
            "name": "Other",
            "description": "A percentages question that fits none of the subtopics above.",
        },
    ],
    "Converting between ratios, fractions, decimals and percentages": [
        {
            "name": "Quantities as fractions and ratios",
            "description": "Writing one quantity as a fraction of another, or converting between a ratio and a fraction, e.g. boys:girls = 2:3 so 2/5 are boys.",
        },
        {
            "name": "Converting fractions, decimals and percentages",
            "description": "Converting between fractions, decimals and percentages, or ordering a mixed list of them.",
        },
        {
            "name": "Other",
            "description": "A conversion question that fits none of the subtopics above.",
        },
    ],
    "Proportion": [
        {
            "name": "Direct proportion",
            "description": "Problems where two quantities increase at the same rate, e.g. best buys, recipes or the unitary method.",
        },
        {
            "name": "Inverse proportion",
            "description": "Problems where one quantity increases as the other decreases, e.g. more workers finish a job faster.",
        },
        {
            "name": "Proportion equations",
            "description": "Forming and using equations such as y = kx^2 or y = k/x from a proportionality statement.",
        },
        {
            "name": "Proportion graphs",
            "description": "Recognising or sketching graphs that show direct or inverse proportion.",
        },
        {
            "name": "Other",
            "description": "A proportion question that fits none of the subtopics above.",
        },
    ],
    "Rates and compound units": [
        {
            "name": "Speed, distance and time",
            "description": "Using speed = distance / time, including average speed and converting between units such as km/h and m/s.",
        },
        {"name": "Density", "description": "Using density = mass / volume."},
        {"name": "Pressure", "description": "Using pressure = force / area."},
        {
            "name": "Rates of pay and unit pricing",
            "description": "Rates such as hourly pay, flow rates, or price per unit to compare value for money.",
        },
        {
            "name": "Other",
            "description": "A rates or compound units question that fits none of the subtopics above.",
        },
    ],
    "Angles and polygons": [
        {
            "name": "Geometry vocabulary and notation",
            "description": "Naming angles, lines and shapes, e.g. acute, obtuse, reflex, or using notation such as angle ABC.",
        },
        {
            "name": "Angles at a point and on a line",
            "description": "Using angles on a straight line sum to 180, angles round a point sum to 360, and vertically opposite angles.",
        },
        {
            "name": "Angles in parallel lines",
            "description": "Finding angles using alternate, corresponding and co-interior angles, usually giving reasons.",
        },
        {
            "name": "Angles in triangles and quadrilaterals",
            "description": "Using the angle sums of triangles (180) and quadrilaterals (360) to find missing angles.",
        },
        {
            "name": "Interior and exterior angles of polygons",
            "description": "Finding interior or exterior angles of polygons, or the number of sides from an angle.",
        },
        {
            "name": "Properties of triangles and quadrilaterals",
            "description": "Properties of shapes such as isosceles triangles, parallelograms, rhombuses and kites, including symmetry.",
        },
        {
            "name": "Geometric proof",
            "description": "Proving an angle or geometric fact with a chain of reasons. Not for circle theorems or congruence proofs.",
        },
        {
            "name": "Other",
            "description": "An angles or polygons question that fits none of the subtopics above.",
        },
    ],
    "Constructions and loci": [
        {
            "name": "Ruler and compass constructions",
            "description": "Constructing perpendicular bisectors, angle bisectors, perpendiculars from a point, or triangles with a ruler and compasses.",
        },
        {
            "name": "Loci",
            "description": "Drawing or shading the set of points that meet conditions, e.g. within 3 m of a point or closer to A than B.",
        },
        {
            "name": "Bearings",
            "description": "Measuring, drawing or calculating three-figure bearings, including back bearings.",
        },
        {
            "name": "Measuring lines and angles",
            "description": "Measuring lengths with a ruler or angles with a protractor, or drawing them accurately.",
        },
        {
            "name": "Other",
            "description": "A constructions or loci question that fits none of the subtopics above.",
        },
    ],
    "Transformations": [
        {
            "name": "Reflection",
            "description": "Reflecting a shape in a line, or describing a reflection by giving the mirror line's equation.",
        },
        {
            "name": "Rotation",
            "description": "Rotating a shape, or describing a rotation by its angle, direction and centre.",
        },
        {
            "name": "Translation",
            "description": "Translating a shape by a column vector, or describing a translation with a vector.",
        },
        {
            "name": "Enlargement",
            "description": "Enlarging a shape by a positive whole or fractional scale factor from a centre, or describing an enlargement.",
        },
        {
            "name": "Enlargement with negative scale factors",  # Higher only
            "description": "Enlarging by a negative scale factor, which places the image on the other side of the centre, inverted. Higher tier.",
        },
        {
            "name": "Combined transformations",  # Higher only
            "description": "Applying two transformations in turn and describing the single transformation that is equivalent. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A transformations question that fits none of the subtopics above.",
        },
    ],
    "Congruence and similarity": [
        {
            "name": "Congruent triangles",
            "description": "Identifying congruent shapes, or proving triangles are congruent with SSS, SAS, ASA or RHS.",
        },
        {
            "name": "Similar shapes",
            "description": "Finding missing lengths in similar shapes using a length scale factor, or showing shapes are similar.",
        },
        {
            "name": "Area and volume scale factors",  # Higher only
            "description": "Using the fact that area scales by k^2 and volume by k^3 for similar shapes or solids. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A congruence or similarity question that fits none of the subtopics above.",
        },
    ],
    "Circles": [
        {
            "name": "Circle terms and properties",
            "description": "Naming parts of a circle, e.g. radius, chord, tangent, arc, sector, segment.",
        },
        {
            "name": "Circumference and area of circles",
            "description": "Calculating the circumference or area of a circle, semicircle or quarter circle, or working backwards to the radius.",
        },
        {
            "name": "Arc length and sector area",
            "description": "Calculating arc lengths, sector areas or perimeters of sectors using the angle at the centre.",
        },
        {
            "name": "Circle theorems",  # Higher only
            "description": "Finding angles or proving results with circle theorems, e.g. angle in a semicircle, cyclic quadrilaterals, alternate segment. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A circles question that fits none of the subtopics above.",
        },
    ],
    "Area and volume": [
        {
            "name": "Area of triangles, parallelograms and trapezia",
            "description": "Calculating the area of rectangles, triangles, parallelograms or trapezia using the standard formulae.",
        },
        {
            "name": "Perimeter and area of composite shapes",
            "description": "Perimeter or area of shapes made by combining or removing simple shapes, including word problems such as paint or tiles.",
        },
        {
            "name": "Volume of prisms and cylinders",
            "description": "Calculating the volume of cuboids, prisms or cylinders, or capacity problems such as filling a tank.",
        },
        {
            "name": "Surface area",
            "description": "Calculating the total surface area of cuboids, prisms, cylinders, cones or spheres.",
        },
        {
            "name": "Volume of pyramids, cones and spheres",
            "description": "Calculating volumes of pyramids, cones, spheres, hemispheres or frustums, usually with given formulae.",
        },
        {
            "name": "Properties of 3D shapes",
            "description": "Faces, edges and vertices of 3D shapes, or drawing and recognising nets.",
        },
        {
            "name": "Plans and elevations",
            "description": "Drawing or interpreting plan, front and side elevations of 3D shapes, or isometric drawings.",
        },
        {
            "name": "Other",
            "description": "An area or volume question that fits none of the subtopics above.",
        },
    ],
    "Pythagoras and trigonometry": [
        {
            "name": "Pythagoras' theorem",
            "description": "Finding a missing side of a right-angled triangle with a^2 + b^2 = c^2, or the distance between two points.",
        },
        {
            "name": "Trigonometry in right-angled triangles",
            "description": "Finding a side or angle in a right-angled triangle using sin, cos or tan (SOHCAHTOA), including angles of elevation.",
        },
        {
            "name": "Exact trigonometric values",
            "description": "Knowing exact values of sin, cos and tan for 0, 30, 45, 60 and 90 degrees without a calculator.",
        },
        {
            "name": "Pythagoras and trigonometry in 3D",  # Higher only
            "description": "Using Pythagoras or trigonometry in 3D shapes, e.g. the space diagonal of a cuboid or the angle between a line and a plane. Higher tier.",
        },
        {
            "name": "Sine rule",  # Higher only
            "description": "Finding a side or angle in a non-right-angled triangle with a/sinA = b/sinB. Higher tier.",
        },
        {
            "name": "Cosine rule",  # Higher only
            "description": "Finding a side or angle in a non-right-angled triangle with a^2 = b^2 + c^2 - 2bc cosA. Higher tier.",
        },
        {
            "name": "Area of a triangle using sine",  # Higher only
            "description": "Finding the area of a triangle with area = 1/2 ab sinC. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A Pythagoras or trigonometry question that fits none of the subtopics above.",
        },
    ],
    "Vectors": [
        {
            "name": "Vector notation and arithmetic",
            "description": "Column vectors, adding, subtracting and multiplying vectors by a scalar, or writing a path between points as a vector.",
        },
        {
            "name": "Vector proofs",  # Higher only
            "description": "Using vectors to prove that points are collinear or lines are parallel, often with points dividing a line in a ratio. Higher tier.",
        },
        {
            "name": "Other",
            "description": "A vectors question that fits none of the subtopics above.",
        },
    ],
    "Probability": [
        {
            "name": "Probability scale and basic probability",
            "description": "Probabilities of single events, the 0 to 1 scale, and using that probabilities of all outcomes sum to 1.",
        },
        {
            "name": "Relative frequency and experiments",
            "description": "Estimating a probability from experimental results, e.g. a biased dice rolled many times.",
        },
        {
            "name": "Expected outcomes",
            "description": "Working out how many times an outcome is expected to happen, probability x number of trials.",
        },
        {
            "name": "Frequency trees",
            "description": "Completing or using a branching diagram of counts (not probabilities) to answer questions.",
        },
        {
            "name": "Sample space diagrams",
            "description": "Listing all outcomes of two events in a table or grid, e.g. two dice, and finding probabilities from it.",
        },
        {
            "name": "Venn diagrams",
            "description": "Completing or using Venn diagrams, including set notation such as union, intersection and complement.",
        },
        {
            "name": "Tree diagrams",
            "description": "Drawing or using probability tree diagrams for two or more events, with or without replacement.",
        },
        {
            "name": "Independent and dependent events",
            "description": "Using P(A and B) = P(A) x P(B) for independent events, or deciding whether events are independent.",
        },
        {
            "name": "Conditional probability",  # Higher only
            "description": "Probability of an event given that another has happened, from Venn diagrams, tables or trees, e.g. P(A|B). Higher tier.",
        },
        {
            "name": "Other",
            "description": "A probability question that fits none of the subtopics above.",
        },
    ],
    "Data and sampling": [
        {
            "name": "Sampling",
            "description": "Populations and samples, bias, random and stratified sampling, or capture-recapture estimates.",
        },
        {
            "name": "Frequency tables",
            "description": "Completing or reading a table of tallies and counts, including grouped frequency tables. Not for calculating averages.",
        },
        {
            "name": "Two-way tables",
            "description": "Completing or reading a table that classifies data by two categories, e.g. gender and favourite sport.",
        },
        {
            "name": "Other",
            "description": "A data or sampling question that fits none of the subtopics above.",
        },
    ],
    "Charts and graphs": [
        {
            "name": "Bar charts and pictograms",
            "description": "Drawing or interpreting bar charts, composite or dual bar charts, line graphs, or pictograms.",
        },
        {
            "name": "Pie charts",
            "description": "Drawing or interpreting pie charts, including working out angles from frequencies.",
        },
        {
            "name": "Time series graphs",
            "description": "Plotting or interpreting data over time, describing trends or seasonal patterns.",
        },
        {
            "name": "Stem and leaf diagrams",
            "description": "Drawing or reading stem and leaf diagrams, including finding averages and range from them.",
        },
        {
            "name": "Frequency polygons",
            "description": "Drawing or interpreting a line graph that joins the midpoints of grouped frequency classes.",
        },
        {
            "name": "Histograms",  # Higher only
            "description": "Histograms with unequal class widths using frequency density, drawing them or estimating frequencies from them. Higher tier.",
        },
        {
            "name": "Cumulative frequency",  # Higher only
            "description": "Running totals from a grouped table, drawing the cumulative frequency graph, and reading the median and quartiles off it. Higher tier.",
        },
        {
            "name": "Box plots",  # Higher only
            "description": "Drawing or interpreting box plots from the minimum, quartiles, median and maximum, often to compare data sets. Higher tier.",
        },
        {
            "name": "Scatter graphs",
            "description": "Plotting scatter graphs, describing correlation, drawing a line of best fit, estimating from it, or identifying outliers.",
        },
        {
            "name": "Other",
            "description": "A charts or graphs question that fits none of the subtopics above.",
        },
    ],
    "Averages and spread": [
        {
            "name": "Mean, median, mode and range",
            "description": "Calculating averages and range from a list of data, or working backwards, e.g. finding a missing value from the mean.",
        },
        {
            "name": "Averages from frequency tables",
            "description": "Mean, median, mode or range calculated from a frequency table, including estimating the mean of grouped data.",
        },
        {
            "name": "Quartiles and interquartile range",  # Higher only
            "description": "Finding the lower and upper quartiles and the interquartile range from a list or diagram. Higher tier.",
        },
        {
            "name": "Comparing distributions",
            "description": "Comparing two data sets with an average and a measure of spread, written in context.",
        },
        {
            "name": "Other",
            "description": "An averages or spread question that fits none of the subtopics above.",
        },
    ],
}

HIGHER_ONLY = {
    "Product rule for counting",
    "Estimating powers and roots",
    "Fractional indices",
    "Surds",
    "Rationalising denominators",
    "Recurring decimals to fractions",
    "Upper and lower bounds",
    "Factorising non-monic quadratics",
    "Algebraic fractions",
    "Algebraic proof",
    "Inverse and composite functions",
    "Graph transformations",
    "Exponential graphs",
    "Trigonometric graphs",
    "Gradients and areas under curves",
    "Equation of a circle",
    "Completing the square",
    "Quadratic formula",
    "Simultaneous equations with a quadratic",
    "Iteration",
    "Quadratic inequalities",
    "Inequalities on graphs",
    "Enlargement with negative scale factors",
    "Combined transformations",
    "Area and volume scale factors",
    "Circle theorems",
    "Pythagoras and trigonometry in 3D",
    "Sine rule",
    "Cosine rule",
    "Area of a triangle using sine",
    "Vector proofs",
    "Conditional probability",
    "Histograms",
    "Cumulative frequency",
    "Box plots",
    "Quartiles and interquartile range",
}

CATEGORY_DESCRIPTIONS = {
    "Number basics": "Ordering numbers, negatives, the four operations, place value and order of operations.",
    "Factors, multiples and primes": "Primes, factors, multiples, HCF, LCM and prime factorisation.",
    "Powers, roots and standard form": "Powers, roots, indices, surds and standard form.",
    "Fractions": "Calculating with fractions and mixed numbers, and finding fractions of amounts.",
    "Converting between ratios, fractions, decimals and percentages": "Changing a quantity from one of these forms into another.",
    "Estimation and accuracy": "Estimating, rounding, error intervals and bounds.",
    "Units and measures": "Standard units and converting between them.",
    "Algebraic expressions": "Simplifying, expanding and factorising expressions, indices and algebraic proof.",
    "Formulae and functions": "Substituting into and rearranging formulae, and function notation.",
    "Graphs": "Plotting, sketching and interpreting graphs, including straight-line and real-life graphs.",
    "Equations and inequalities": "Solving linear, quadratic and simultaneous equations, and inequalities.",
    "Sequences": "Continuing sequences and finding nth term rules.",
    "Ratio": "Simplifying and sharing in ratios, and using scale.",
    "Percentages": "Percentage of an amount, increase and decrease, and interest.",
    "Proportion": "Direct and inverse proportion.",
    "Rates and compound units": "Speed, density, pressure and other rates.",
    "Angles and polygons": "Angle facts, parallel lines, polygons and geometric properties.",
    "Constructions and loci": "Ruler and compass constructions, loci and bearings.",
    "Transformations": "Reflecting, rotating, translating and enlarging shapes.",
    "Congruence and similarity": "Congruent and similar shapes, and scale factors for lengths, areas and volumes.",
    "Circles": "Circle parts, circumference, area, sectors and circle theorems.",
    "Area and volume": "Perimeter, area, surface area and volume of 2D and 3D shapes.",
    "Pythagoras and trigonometry": "Pythagoras, sin, cos, tan, and the sine and cosine rules.",
    "Vectors": "Vector notation, arithmetic and proof.",
    "Probability": "Probability scale, experiments, tree diagrams, Venn diagrams and conditional probability.",
    "Data and sampling": "Sampling and organising data in tables.",
    "Charts and graphs": "Drawing and reading statistical charts, histograms and scatter graphs.",
    "Averages and spread": "Mean, median, mode, range and quartiles, and comparing distributions.",
}
