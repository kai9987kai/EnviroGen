from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    category: str
    title: str
    source: str
    format: str
    url: str
    why: str


RESOURCE_CATALOG: tuple[Resource, ...] = (
    Resource("ABM fundamentals", "Introduction to Agent-Based Modeling", "Complexity Explorer / Santa Fe Institute", "Course", "https://www.complexityexplorer.org/", "A structured learning path for bottom-up simulation thinking."),
    Resource("ABM fundamentals", "Agent Based Modeling", "TU Delft OpenCourseWare", "Lecture video", "https://ocw.tudelft.nl/course-lectures/agent-based-modeling/", "Introduces agents, generative science, and bottom-up modeling."),
    Resource("ABM fundamentals", "Agent-based model overview", "Wikipedia", "Reference", "https://en.wikipedia.org/wiki/Agent-based_model", "Quick vocabulary for agents, rules, emergence, and applications."),
    Resource("ABM fundamentals", "Agent-based model in biology", "Wikipedia", "Reference", "https://en.wikipedia.org/wiki/Agent-based_model_in_biology", "Useful context for ecology and biological simulations."),
    Resource("ABM fundamentals", "Introductory Tutorial on Agent-Based Modeling", "SBP-BRiMS", "Tutorial PDF", "https://sbp-brims.org/2025/tutorial/Macal-2025.pdf", "Compact tutorial framing for scientific ABM practice."),
    Resource("ABM fundamentals", "Agent-Based Modelling tutorial", "Jill Badham", "Tutorial PDF", "https://jbadham.biz/Research/ABMBook/ABMtutorial.pdf", "Practical tutorial concepts that translate into small simulations."),
    Resource("ABM fundamentals", "Model Thinking", "University of Michigan / Scott Page", "Course", "https://www.coursera.org/learn/model-thinking", "Covers model reasoning, tipping points, contagion, and social dynamics."),
    Resource("ABM fundamentals", "Agent-Based and Individual-Based Modeling", "Railsback and Grimm", "Book site", "https://www.railsback-grimm-abm-book.com/", "Canonical ABM and IBM methodology for ecological simulations."),
    Resource("ABM fundamentals", "CoMSES Education Resources", "CoMSES Network", "Resource hub", "https://www.comses.net/resources/education/", "Community-curated teaching material for computational modeling."),
    Resource("ABM fundamentals", "CoMSES Computational Model Library", "CoMSES Network", "Model library", "https://www.comses.net/codebases/", "Citable ABM codebases for implementation comparison."),
    Resource("ABM fundamentals", "Open Modeling Foundation Standards", "Open Modeling Foundation", "Standards", "https://www.openmodelingfoundation.org/standards/", "Guidance for transparent and reusable computational models."),
    Resource("Mesa", "Mesa documentation", "Project Mesa", "Docs", "https://mesa.readthedocs.io/stable/", "Current Python ABM reference for model structure and analysis."),
    Resource("Mesa", "Mesa getting started", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/getting_started.html", "Shows core concepts, activation, space, data collection, and visualization."),
    Resource("Mesa", "Creating your first Mesa model", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/0_first_model.html", "Useful baseline for designing small Python ABMs."),
    Resource("Mesa", "Mesa AgentSet tutorial", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/1_agentset.html", "Good reference for managing collections of agents."),
    Resource("Mesa", "Mesa agent activation", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/2_agent_activation.html", "Explains scheduling choices and their effect on outcomes."),
    Resource("Mesa", "Mesa event scheduling", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/3_event_scheduling.html", "Reference for time and event design in simulations."),
    Resource("Mesa", "Mesa data collection", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/6_collecting_data.html", "Useful for metrics and experiment exports."),
    Resource("Mesa", "Mesa parameter sweeps", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/9_parameter_sweeps.html", "Directly relevant to EnviroGen batch experiments."),
    Resource("Mesa", "Mesa examples repository", "Project Mesa", "Examples", "https://github.com/projectmesa/mesa-examples", "Model examples for comparing EnviroGen scenarios."),
    Resource("Mesa", "AgentPy documentation", "AgentPy", "Docs", "https://agentpy.readthedocs.io/en/latest/", "Python ABM framework focused on experiments and analysis."),
    Resource("Mesa", "Repast Suite documentation", "Argonne National Laboratory", "Docs", "https://repast.github.io/docs.html", "Mature ABM framework reference for batch and distributed simulation."),
    Resource("Mesa", "GAMA tutorials", "GAMA Platform", "Tutorials", "https://gama-platform.org/wiki/Tutorials", "Spatial ABM tutorials with ecology, GIS, and 3D examples."),
    Resource("Mesa", "FLAME GPU user guide", "FLAME GPU", "Docs", "https://flamegpu.readthedocs.io/en/master/", "Reference point for GPU-scale agent simulations."),
    Resource("NetLogo", "NetLogo Models Library", "Northwestern CCL", "Model library", "https://ccl.northwestern.edu/netlogo/models/", "Classic ecology and emergence examples."),
    Resource("NetLogo", "NetLogo User Manual", "Northwestern CCL", "Docs", "https://docs.netlogo.org/", "Mature reference for agent-based teaching interfaces."),
    Resource("NetLogo", "NetLogo Tutorial 1", "Northwestern CCL", "Tutorial", "https://docs.netlogo.org/7.0.3/tutorial1.html", "First steps with agents and the interface."),
    Resource("NetLogo", "NetLogo Tutorial 2", "Northwestern CCL", "Tutorial", "https://docs.netlogo.org/7.0.3/tutorial2.html", "Hands-on commands and agent inspection."),
    Resource("NetLogo", "NetLogo Tutorial 3", "Northwestern CCL", "Tutorial", "https://docs.netlogo.org/7.0.3/tutorial3.html", "Builds a complete model in stages."),
    Resource("NetLogo", "NetLogo Programming Guide", "Northwestern CCL", "Docs", "https://docs.netlogo.org/programming.html", "Reference for tick-based modeling conventions."),
    Resource("NetLogo", "NetLogo Modeling Commons", "NetLogo community", "Model community", "https://modelingcommons.org/", "Community models and inspiration for new scenarios."),
    Resource("NetLogo", "NetLogo Web", "Northwestern CCL", "Web app", "https://netlogoweb.org/", "Browser-based model running and sharing."),
    Resource("NetLogo", "BehaviorSpace guide", "NetLogo", "Docs", "https://docs.netlogo.org/behaviorspace.html", "Official parameter sweep tooling for NetLogo experiments."),
    Resource("NetLogo", "BehaviorSearch", "NetLogo ecosystem", "Tool", "https://www.behaviorsearch.org/", "Searches model parameter spaces for target behavior."),
    Resource("NetLogo", "NetLogo GIS extension", "NetLogo", "Docs", "https://docs.netlogo.org/gis.html", "Adds spatial data integration for ecology simulations."),
    Resource("Artificial life", "Artificial Life journal", "MIT Press", "Research videos/articles", "https://direct.mit.edu/artl", "Research context for emergent behavior and evolution."),
    Resource("Artificial life", "Emergent Resource Exchange and Tolerated Theft Behavior", "Artificial Life / MIT Press", "Research article", "https://direct.mit.edu/artl/article/30/1/28/119154/Emergent-Resource-Exchange-and-Tolerated-Theft", "Example of multi-agent resource dynamics."),
    Resource("Artificial life", "Origins of Life", "Complexity Explorer", "Course", "https://www.complexityexplorer.org/", "Broader complex-systems framing for emergence."),
    Resource("Artificial life", "Introduction to Complexity", "Complexity Explorer", "Course", "https://www.complexityexplorer.org/", "Core concepts: feedback, adaptation, scaling, emergence."),
    Resource("Artificial life", "Computation in Complex Systems", "Complexity Explorer", "Course", "https://www.complexityexplorer.org/", "Useful computational grounding for simulation experiments."),
    Resource("Artificial life", "The Nature of Code", "Daniel Shiffman", "Book", "https://natureofcode.com/", "Practical natural-systems simulation: agents, evolution, and neural ideas."),
    Resource("Artificial life", "The Nature of Code video track", "The Coding Train", "Video series", "https://thecodingtrain.com/tracks/the-nature-of-code-2/", "Large companion video series for natural systems simulation."),
    Resource("Artificial life", "Avida-ED", "Avida-ED Project", "Interactive curriculum", "https://avida-ed.github.io/", "Digital evolution curriculum and interactive experiments."),
    Resource("Ecology simulation", "Wolf Sheep Predation model", "NetLogo Models Library", "Model", "https://ccl.northwestern.edu/netlogo/models/WolfSheepPredation", "Canonical predator-resource population dynamics reference."),
    Resource("Ecology simulation", "Fire model", "NetLogo Models Library", "Model", "https://ccl.northwestern.edu/netlogo/models/Fire", "Simple local-rule model with emergent spread behavior."),
    Resource("Ecology simulation", "Ant Lines model", "NetLogo Models Library", "Model", "https://ccl.northwestern.edu/netlogo/models/AntLines", "Good local-sensing and stigmergy inspiration."),
    Resource("Ecology simulation", "Life model", "NetLogo Models Library", "Model", "https://ccl.northwestern.edu/netlogo/models/Life", "Minimal cellular emergence model."),
    Resource("Ecology simulation", "Plant-animal interactions in ABM", "Agent-based model in biology", "Reference", "https://en.wikipedia.org/wiki/Agent-based_model_in_biology", "Examples of ecological agent interactions."),
    Resource("Ecology simulation", "Modeling Environmental Complexity", "MIT OpenCourseWare", "Course", "https://ocw.mit.edu/courses/12-086-modeling-environmental-complexity-fall-2014/", "Environmental modeling course with biological and physical systems."),
    Resource("Ecology simulation", "Landlab tutorials", "CSDMS / Landlab", "Tutorials", "https://landlab.readthedocs.io/en/latest/tutorials/index.html", "Earth-surface and ecological process simulation tutorials."),
    Resource("Ecology simulation", "CSDMS Labs Portal", "CSDMS", "Teaching labs", "https://csdms.colorado.edu/wiki/Labs_portal", "Environmental and surface-dynamics modeling labs."),
    Resource("Experiments and optimization", "Mesa BatchRunner and parameter sweeps", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/9_parameter_sweeps.html", "Practical design for repeatable multi-seed runs."),
    Resource("Experiments and optimization", "Comparing scenarios", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/10_comparing_scenarios.html", "Guidance for interpreting experiment outcomes."),
    Resource("Experiments and optimization", "Large-scale ABM on cloud infrastructure", "arXiv", "Research article", "https://arxiv.org/abs/2602.15317", "Shows why performance and reproducibility matter as models scale."),
    Resource("Experiments and optimization", "NL4Py parallelizable NetLogo workspaces", "arXiv", "Research article", "https://arxiv.org/abs/1808.03292", "Useful perspective on batch and parallel simulation workflows."),
    Resource("Experiments and optimization", "SALib documentation", "SALib contributors", "Docs", "https://salib.readthedocs.io/en/latest/", "Sensitivity analysis for simulation inputs and outcomes."),
    Resource("Experiments and optimization", "EMA Workbench tutorials", "TU Delft / EMA Workbench", "Tutorials", "https://emaworkbench.readthedocs.io/en/latest/", "Exploratory modeling and uncertainty analysis workflows."),
    Resource("Experiments and optimization", "Optuna tutorials", "Optuna contributors", "Tutorials", "https://optuna.readthedocs.io/en/stable/tutorial/index.html", "Modern optimization workflows for calibration."),
    Resource("Experiments and optimization", "SciPy optimize tutorial", "SciPy", "Tutorial", "https://docs.scipy.org/doc/scipy/tutorial/optimize.html", "Core optimization methods for fitting and calibration."),
    Resource("Visualization", "Mesa basic visualization", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/7_visualization_basic.html", "Reference for interactive model views."),
    Resource("Visualization", "Mesa dynamic agent visualization", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/7_visualization_dynamic.html", "Ideas for changing visuals as agent state changes."),
    Resource("Visualization", "Mesa SpaceRenderer", "Project Mesa", "Tutorial", "https://mesa.readthedocs.io/stable/tutorials/8_space_renderer.html", "Reference for richer spatial visualization."),
    Resource("Visualization", "LLM empowered agent-based modeling survey", "Nature Humanities and Social Sciences Communications", "Survey", "https://www.nature.com/articles/s41599-024-03611-3", "Explains modern optional AI-agent directions without making them default."),
    Resource("Visualization", "Bokeh example gallery", "Bokeh", "Examples", "https://docs.bokeh.org/en/latest/docs/examples.html", "Interactive plotting and dashboard examples."),
    Resource("Visualization", "Panel tutorials", "HoloViz / Panel", "Tutorials", "https://panel.holoviz.org/tutorials/index.html", "Parameter-control dashboard patterns for simulations."),
    Resource("Visualization", "Plotly Python getting started", "Plotly", "Docs", "https://plotly.com/python/getting-started/", "Interactive charts for simulation metrics."),
)


def resources_by_category() -> dict[str, list[Resource]]:
    grouped: dict[str, list[Resource]] = {}
    for resource in RESOURCE_CATALOG:
        grouped.setdefault(resource.category, []).append(resource)
    return grouped
