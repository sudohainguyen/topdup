import React, { useEffect, useState } from "react"
import { IconContext } from "react-icons"
import { FaCheck, FaHashtag, FaTimes } from "react-icons/fa"
import useUserData from "../../shared/useUserData"
import DupReportService from "./dup-report.service"

export const DupReportList = (props) => {
  const [simReports, setSimReports] = useState({ ...props.simReports })
  const [loading, setLoading] = useState({ ...props.loading })
  const { userData, setUserData } = useUserData()
  const dupReportService = new DupReportService()

  useEffect(() => setSimReports(props.simReports), [props.simReports])
  useEffect(() => setLoading(props.loading), [props.loading])

  if (loading) {
    return (
      <div className="sr-list-container centered-container">
        <h2>Loading...</h2>
      </div>
    )
  }

  const iconRenderer = (IconComponent, color) => {
    return (
      <IconContext.Provider value={{ color: color, className: "global-class-name" }}>
        <IconComponent />
      </IconContext.Provider>
    )
  }

  const applyVote = (simReport, votedOption) => {
    const userId = userData && userData.user && userData.user.id
    dupReportService.applyVote(simReport, votedOption, userId)
      .then(result => {
        const updatedSimReport = result.data
        const updatedSimReports = simReports.map(item => {
          if (item.id !== simReport.id) return item
          return { ...item, ...updatedSimReport }
        })
        setSimReports(updatedSimReports)
      })
      .catch(error => {
        throw (error)
      })
  }

  const reportRowRenderer = simReport => {
    const voteItemClassName = value => "sr-vote-item " + (simReport["votedOption"] === value ? "selected" : "")
    return (
      <div className="sim-report-row">
        <div className="sr-title-container">
          <div className="sr-title">
            <span>{simReport["articleAId"]}{simReport["articleA"]}</span>
          </div>
          <div className="sr-title">
            <span>{simReport["articleBId"]}{simReport["articleB"]}</span>
          </div>
        </div>
        <div className="sr-vote-container">
          <div className="sr-vote-check-container">
            <div className={voteItemClassName(1)}>
              <button className="btn btn-outline-secondary btn-sm sr-vote-btn"
                disabled={!userData}
                onClick={() => applyVote(simReport, 1)}>
                {simReport["articleANbVotes"]}&nbsp;{iconRenderer(FaCheck, "#3571FF")}
              </button>
            </div>
            <div className={voteItemClassName(2)}>
              <button disabled={!userData}
                className="btn btn-outline-secondary btn-sm sr-vote-btn"
                onClick={() => applyVote(simReport, 2)}>
                {simReport["articleBNbVotes"]}&nbsp;{iconRenderer(FaCheck, "#3571FF")}
              </button>
            </div>
          </div>
          <div className={voteItemClassName(3)}>
            <button className="btn btn-outline-secondary btn-sm sr-vote-error-btn"
              disabled={!userData}
              onClick={() => applyVote(simReport, 3)}>
              {iconRenderer(FaTimes, "#EF5A5A")}
            </button>
          </div>
          <div className={voteItemClassName(4)}>
            <button className="btn btn-outline-secondary btn-sm sr-vote-irrelevant-btn"
              disabled={!userData}
              onClick={() => applyVote(simReport, 4)}>
              {iconRenderer(FaHashtag, "#F69E0C")}
            </button>
          </div>
        </div>
        <div className="sr-domain-date">
          <div className="col-sm-6">

            <div className="row other">{simReport["domainA"]}</div>
            <div className="row other">{simReport["domainB"]}</div>
          </div>
          <div className="col-sm-6">
            <div className="row other">{new Date(simReport["createdDateA"]).toLocaleDateString()}</div>
            <div className="row other">{new Date(simReport["createdDateB"]).toLocaleDateString()}</div>
          </div>
        </div>
        <div className="sr-compare">
          <button className="btn btn-outline-secondary">So sánh</button>
        </div>
      </div>
    )
  }

  return <div className="sr-list-container">{simReports.map(item => reportRowRenderer(item))}</div>
}

export default DupReportList