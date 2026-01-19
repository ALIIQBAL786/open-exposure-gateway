{{/*
Expand the name of the chart.
*/}}
{{- define "srm.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "srm.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "srm.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "srm.labels" -}}
helm.sh/chart: {{ include "srm.chart" . }}
{{ include "srm.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "srm.selectorLabels" -}}
app.kubernetes.io/name: {{ include "srm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
MongoDB labels
*/}}
{{- define "srm.mongodb.labels" -}}
helm.sh/chart: {{ include "srm.chart" . }}
{{ include "srm.mongodb.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
MongoDB selector labels
*/}}
{{- define "srm.mongodb.selectorLabels" -}}
app.kubernetes.io/name: {{ .Values.mongodb.name }}
app.kubernetes.io/instance: {{ .Release.Name }}
io.kompose.service: {{ .Values.mongodb.name }}
{{- end }}

{{/*
SRM Controller labels
*/}}
{{- define "srm.controller.labels" -}}
helm.sh/chart: {{ include "srm.chart" . }}
{{ include "srm.controller.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
SRM Controller selector labels
*/}}
{{- define "srm.controller.selectorLabels" -}}
app.kubernetes.io/name: {{ .Values.srmcontroller.name }}
app.kubernetes.io/instance: {{ .Release.Name }}
io.kompose.service: {{ .Values.srmcontroller.name }}
{{- end }}

{{/*
Artifact Manager labels
*/}}
{{- define "srm.artifactmanager.labels" -}}
helm.sh/chart: {{ include "srm.chart" . }}
{{ include "srm.artifactmanager.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Artifact Manager selector labels
*/}}
{{- define "srm.artifactmanager.selectorLabels" -}}
app: {{ .Values.artifactManager.name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Return the proper namespace
*/}}
{{- define "srm.namespace" -}}
{{- default .Release.Namespace .Values.global.namespace }}
{{- end }}
