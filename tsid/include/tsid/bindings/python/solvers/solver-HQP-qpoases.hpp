//
// Copyright (c) 2018 CNRS
//
// This file is part of tsid
// tsid is free software: you can redistribute it
// and/or modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation, either version
// 3 of the License, or (at your option) any later version.
// tsid is distributed in the hope that it will be
// useful, but WITHOUT ANY WARRANTY; without even the implied warranty
// of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// General Lesser Public License for more details. You should have
// received a copy of the GNU Lesser General Public License along with
// tsid If not, see
// <http://www.gnu.org/licenses/>.
//

#ifndef __tsid_python_solver_qpoases_hpp__
#define __tsid_python_solver_qpoases_hpp__

#include "tsid/bindings/python/fwd.hpp"

#include "tsid/solvers/solver-HQP-qpoases.hpp"
#include "tsid/solvers/solver-HQP-output.hpp"
#include "tsid/solvers/fwd.hpp"
#include "tsid/bindings/python/utils/container.hpp"

namespace tsid
{
  namespace python
  {    
    namespace bp = boost::python;
    
    template<typename Solver>
    struct SolverHQPOASESPythonVisitor
    : public boost::python::def_visitor< SolverHQPOASESPythonVisitor<Solver> >
    {
      template<class PyClass>     

      void visit(PyClass& cl) const
      {
        cl
        .def(bp::init<std::string>((bp::arg("name")), "Default Constructor with name"))
        
        .def("resize", &SolverHQPOASESPythonVisitor::resize, bp::args("n", "neq", "nin"))
        .add_property("ObjVal", &Solver::getObjectiveValue, "return obj value")
        .def("solve", &SolverHQPOASESPythonVisitor::solve, bp::args("HQPData"))
        .def("solve", &SolverHQPOASESPythonVisitor::solver_helper, bp::args("HQPData for Python"))

        ;
      }
       
      static void resize(Solver & self, unsigned int n, unsigned int neq, unsigned int nin){
          self.resize(n, neq, nin);
      }  
      static solvers::HQPOutput solve(Solver & self, const solvers::HQPData & problemData){
          solvers::HQPOutput output;
          output = self.solve(problemData);
          return output;
      }
      static solvers::HQPOutput solver_helper(Solver & self, HQPDatas & HQPDatas){
          solvers::HQPOutput output;
          solvers::HQPData data = HQPDatas.get();

          output = self.solve(data);
         
          return output;
      }

      static void expose(const std::string & class_name)
      {
        std::string doc = "Solver QPOases info.";
        bp::class_<Solver>(class_name.c_str(),
                          doc.c_str(),
                          bp::no_init)
        .def(SolverHQPOASESPythonVisitor<Solver>());       
      }
    };
  }
}


#endif // ifndef __tsid_python_solver_qpoases_hpp__
